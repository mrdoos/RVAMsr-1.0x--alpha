import os
import json

class Runner:
    def __init__(self, vertx, networkRunner, natService, jsonRpc, engineJsonRpc, graphQLHttp, webSocketRpc, ipcJsonRpc,
                 stratumServer, metrics, ethStatsService, besuController, dataDir, pidPath, transactionLogBloomCacher,
                 blockchain):
        self.vertx = vertx
        self.networkRunner = networkRunner
        self.natService = natService
        self.graphQLHttp = graphQLHttp
        self.pidPath = pidPath
        self.jsonRpc = jsonRpc
        self.engineJsonRpc = engineJsonRpc
        self.webSocketRpc = webSocketRpc
        self.ipcJsonRpc = ipcJsonRpc
        self.metrics = metrics
        self.ethStatsService = ethStatsService
        self.besuController = besuController
        self.dataDir = dataDir
        self.stratumServer = stratumServer
        self.autoTransactionLogBloomCachingService = \
            AutoTransactionLogBloomCachingService(blockchain, transactionLogBloomCacher)
        self.transactionPoolEvictionService = \
            TransactionPoolEvictionService(vertx, besuController.getTransactionPool())

    def start_external_services(self):
        print("Starting external services...")
        if self.metrics:
            self.wait_for_service_to_start("metrics", self.metrics.start())

        if self.jsonRpc:
            self.wait_for_service_to_start("jsonRpc", self.jsonRpc.start())

        if self.engineJsonRpc:
            self.wait_for_service_to_start("engineJsonRpc", self.engineJsonRpc.start())

        if self.graphQLHttp:
            self.wait_for_service_to_start("graphQLHttp", self.graphQLHttp.start())

        if self.webSocketRpc:
            self.wait_for_service_to_start("webSocketRpc", self.webSocketRpc.start())

        if self.ipcJsonRpc:
            self.wait_for_service_to_start("ipcJsonRpc", self.ipcJsonRpc.start().to_completion_stage().to_completable_future())

        if self.stratumServer:
            self.wait_for_service_to_start("stratum", self.stratumServer.start())

        self.autoTransactionLogBloomCachingService.start()
        if self.ethStatsService:
            self.ethStatsService.start()

    def start_ethereum_main_loop(self):
        try:
            print("Starting Ethereum main loop...")
            self.natService.start()
            self.networkRunner.start()
            if self.networkRunner.get_network().is_p2p_enabled():
                self.besuController.get_synchronizer().start()
            self.besuController.get_mining_coordinator().start()
            self.transactionPoolEvictionService.start()

            print("Ethereum main loop is up.")
            self.write_besu_ports_to_file()
            self.write_besu_networks_to_file()
            self.write_pid_file()
        except Exception as ex:
            print("Unable to start main loop")
            print(ex)
            raise

    def stop(self):
        self.transactionPoolEvictionService.stop()
        if self.jsonRpc:
            self.wait_for_service_to_stop("jsonRpc", self.jsonRpc.stop())

        if self.engineJsonRpc:
            self.wait_for_service_to_stop("engineJsonRpc", self.engineJsonRpc.stop())

        if self.graphQLHttp:
            self.wait_for_service_to_stop("graphQLHttp", self.graphQLHttp.stop())

        if self.webSocketRpc:
            self.wait_for_service_to_stop("webSocketRpc", self.webSocketRpc.stop())

       
