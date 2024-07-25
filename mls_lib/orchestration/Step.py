class Step:
    def __init__(self) -> None:
        self.inputs = dict()
        self.outputs = dict()
        pass

    def execute(self):
        print("Executed abstract Step")
        pass

    def setInput(self, port, value):
        self.inputs[port] = value
    
    def getOutput(self, port):
        return self.outputs[port]

    def __getInput(self, port):
        return self.inputs[port]

    def __setOutput(self, port, value):
        self.outputs[port] = value
