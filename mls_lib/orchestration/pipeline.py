""" Pipeline Class"""
import uuid
class Pipeline:
    """Pipeline: Component that orchestrates a sequence of stages in a pipeline. """
    def __init__(self):
        """
        Initializes a new instance of the class.

        This constructor initializes the `stages` 
        dictionary and calls the constructor of the parent class.

        Parameters:
            None

        Returns:
            None
        """
        super().__init__()
        self.stages = {}
    def add_stage(self, stage, **inputs):
        """
        Adds a stage to the pipeline.

        Parameters:
            stage (Stage): The stage to add to the pipeline.
            inputs (dict): A dictionary of inputs for the stage.

        Returns:
            None
        """
        stage_key = str(uuid.uuid4())
        self.stages[stage_key] = (stage, inputs)

    def clear(self):
        """
        Clears all the stages in the pipeline.

        This method empties the `stages` dictionary, 
        effectively clearing all the stages in the pipeline.

        Parameters:
            None

        Returns:
            None
        """
        self.stages = {}

    def execute(self):
        """
        Executes all the stages in the pipeline.

        This method iterates over the stages in the pipeline, 
        checking if each stage is ready for execution.
        For each ready stage, it collects input data from connected
        input stages and sets the data for the 
        current stage. Once the data is set, it executes the stage
        and marks it as finished. This process 
        continues until all stages in the pipeline have been executed.

        Parameters:
            None

        Returns:
            None
        """
        stage_keys = list(self.stages.keys())
        finish_count = 0
        while finish_count < len(self.stages):
            for stage_key in stage_keys:
                # GROSS TRAVERSE OF STAGES
                if not self.__is_stage_ready(stage_key):
                    continue
                stage, inputs = self.stages[stage_key]
                data = {}
                for port, stage_port in inputs.items():
                    input_stage, input_port = stage_port
                    data[port] = input_stage.get_stage_output(input_port)
                if len(data) > 0:
                    stage.set_data(**data)
                stage.execute()
                stage.finish_execution()
                finish_count += 1
    def __is_stage_ready(self, stage_key):
        """ Checks if the stage is ready to execute. 

        Args:
            stage_key (str): The key of the stage to check.

        Returns:
            bool: True if the stage is ready to execute, False otherwise.
        """
        stage, inputs = self.stages[stage_key]
        # DON't RE RUN FINISHED STAGES
        if stage.is_finished():
            return False
        # DON'T RUN STAGES WITH UNFINISHED INPUTS
        for _, input_stage_port in inputs.items():
            input_stage, _ = input_stage_port
            if not input_stage.is_finished():
                return False
        return True
