#Delay replace pass
class DelayReplace(TransformationPass):
    """Adds delay error information to circuit metadata for noise model post processing"""

    def getNewLabel(self, duration):
        """Generate a unique label based on the duration of the delay

        Args:
            duration (float): the duration of the delay op

        Returns:
            String: the unique label based on duration
        """
        return f'id_delay_{duration}'

    def run(self, dag):
        """Run the DelayReplace pass on 'dag'.

        Args:
            dag (DAGCircuit): the DAG to be optimized

        Returns:
            DAGCircuit: the optimized DAG.
        """

        if not dag.metadata:
            dag.metadata = {}

        if "transpiler_parameterized_error" not in dag.metadata:
            dag.metadata['transpiler_parameterized_error'] = {}

        #iterate over delay nodes
        for node in dag.named_nodes("delay"):
            node_label = self.getNewLabel(node._op.duration)
            node._op.label = node_label


            #save error in metadata
            dag.metadata['transpiler_parameterized_error'][(node_label, tuple(node.qargs))] = [node._op.duration]

        return dag
