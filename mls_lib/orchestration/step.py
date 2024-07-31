class Step:
    def __init__(self, **inputs) -> None:
        self.inputs = inputs
        self.outputs = dict()
        self.finished = False
        pass

    def execute(self):
        raise Exception("Executed abstract Step")
    
    def getOutput(self, port):
        return self.outputs[port]
    
    def _getInputStep(self, port):
        return self.inputs[port]
    
    def isReady(self):
        for _, step in self.inputs.items():
            if not step[0].isFinished():
                return False
        
        return True

    def isFinished(self):
        return self.finished
     
    def _getInput(self, port):
        origin, origin_port = self.inputs[port]
        return origin.getOutput(origin_port)

    def _setOutput(self, port, value):
        self.outputs[port] = value
    
    def finishExecution(self):
        self.finished = True
