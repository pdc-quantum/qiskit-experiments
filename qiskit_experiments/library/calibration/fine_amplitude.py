# This code is part of Qiskit.
#
# (C) Copyright IBM 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Fine amplitude calibration experiment."""

from typing import List, Optional
import numpy as np

from qiskit.circuit import Gate, QuantumCircuit
from qiskit.providers.backend import Backend

from qiskit_experiments.calibration_management import (
    BaseCalibrationExperiment,
    BackendCalibrations,
)
from qiskit_experiments.library.characterization import FineAmplitude
from qiskit_experiments.framework import ExperimentData, Options, fix_class_docs
from qiskit_experiments.calibration_management.update_library import BaseUpdater


@fix_class_docs
class FineAmplitudeCal(BaseCalibrationExperiment, FineAmplitude):
    r"""A calibration version of the :class:`FineAmplitude` experiment.

    # section: overview

        :class:`FineAmplitudeCal` is a subclass of :class:`FineAmplitude`. In the calibration
        experiment the circuits that are run have a custom gate with the pulse schedule attached
        to it through the calibrations.
    """

    def __init__(
        self,
        qubit: int,
        calibrations: BackendCalibrations,
        schedule_name: str,
        backend: Optional[Backend] = None,
        cal_parameter_name: Optional[str] = "amp",
        auto_update: bool = True,
    ):
        """see class :class:`FineAmplitude` for details.

        Args:
            qubit: The qubit for which to run the fine amplitude calibration.
            calibrations: The calibrations instance with the schedules.
            schedule_name: The name of the schedule to calibrate.
            backend: Optional, the backend to run the experiment on.
            cal_parameter_name: The name of the parameter in the schedule to update.
            auto_update: Whether or not to automatically update the calibrations. By
                default this variable is set to True.
            on.
        """
        super().__init__(
            calibrations,
            qubit,
            Gate(name=schedule_name, num_qubits=1, params=[]),
            schedule_name=schedule_name,
            backend=backend,
            cal_parameter_name=cal_parameter_name,
            auto_update=auto_update,
        )

        self.transpile_options.inst_map = calibrations.default_inst_map

    @classmethod
    def _default_experiment_options(cls):
        """Default values for the fine amplitude calibration experiment.

        Experiment Options:
            result_index (int): The index of the result from which to update the calibrations.
            target_angle (float): The target angle of the pulse.
            group (str): The calibration group to which the parameter belongs. This will default
                to the value "default".

        """
        options = super()._default_experiment_options()

        options.result_index = -1
        options.target_angle = np.pi
        options.group = "default"

        return options

    def _add_cal_metadata(self, circuits: List[QuantumCircuit]):
        """Add metadata to the circuit to make the experiment data more self contained.

        The following keys are added to each circuit's metadata:
            cal_param_value: The value of the pulse amplitude. This value together with
                the fit result will be used to find the new value of the pulse amplitude.
            cal_param_name: The name of the parameter in the calibrations.
            cal_schedule: The name of the schedule in the calibrations.
            target_angle: The target angle of the gate.
            cal_group: The calibration group to which the parameter belongs.
        """

        param_val = self._cals.get_parameter_value(
            self._param_name,
            self.physical_qubits,
            self._sched_name,
            group=self.experiment_options.group,
        )

        for circuit in circuits:
            circuit.metadata["cal_param_value"] = param_val
            circuit.metadata["cal_param_name"] = self._param_name
            circuit.metadata["cal_schedule"] = self._sched_name
            circuit.metadata["target_angle"] = self.experiment_options.target_angle
            circuit.metadata["cal_group"] = self.experiment_options.group

        return circuits

    def update_calibrations(self, experiment_data: ExperimentData):
        r"""Update the amplitude of the pulse in the calibrations.

        The update rule of this experiment is

        .. math::

            A \to A \frac{\theta_\text{target}}{\theta_\text{target} + {\rm d}\theta}

        Where :math:`A` is the amplitude of the pulse before the update.

        Args:
            experiment_data: The experiment data from which to extract the measured over/under
                rotation used to adjust the amplitude.
        """
        data = experiment_data.data()

        # No data -> no update
        if len(data) > 0:
            result_index = self.experiment_options.result_index
            group = data[0]["metadata"]["cal_group"]
            target_angle = data[0]["metadata"]["target_angle"]
            prev_amp = data[0]["metadata"]["cal_param_value"]

            d_theta = BaseUpdater.get_value(experiment_data, "d_theta", result_index)

            BaseUpdater.add_parameter_value(
                self._cals,
                experiment_data,
                prev_amp * target_angle / (target_angle + d_theta),
                self._param_name,
                self._sched_name,
                group,
            )


@fix_class_docs
class FineXAmplitudeCal(FineAmplitudeCal):
    """A calibration experiment to calibrate the amplitude of the X schedule."""

    @classmethod
    def _default_experiment_options(cls) -> Options:
        r"""Default values for the fine amplitude experiment.

        Experiment Options:
            add_sx (bool): This option is True by default when calibrating gates with a target
                angle per gate of :math:`\pi` as this increases the sensitivity of the
                experiment.
            add_xp_circuit (bool): This option is True by default when calibrating gates with
                a target angle per gate of :math:`\pi`.
        """
        options = super()._default_experiment_options()
        options.add_sx = True
        options.add_xp_circuit = True

        return options

    @classmethod
    def _default_transpile_options(cls):
        """Default transpile options.

        Transpile Options:
            basis_gates (list(str)): A list of basis gates needed for this experiment.
                The schedules for these basis gates will be provided by the instruction
                schedule map from the calibrations.
        """
        options = super()._default_transpile_options()
        options.basis_gates = ["x", "sx"]

        return options

    @classmethod
    def _default_analysis_options(cls) -> Options:
        """Default analysis options."""
        options = super()._default_analysis_options()
        options.angle_per_gate = np.pi
        options.phase_offset = np.pi / 2

        return options


@fix_class_docs
class FineSXAmplitudeCal(FineAmplitudeCal):
    """A calibration experiment to calibrate the amplitude of the SX schedule."""

    @classmethod
    def _default_experiment_options(cls) -> Options:
        r"""Default values for the fine amplitude experiment.

        Experiment Options:
            add_sx (bool): This option is False by default when calibrating gates with a target
                angle per gate of :math:`\pi/2` as this increases the sensitivity of the
                experiment.
            add_xp_circuit (bool): This option is False by default when calibrating gates with
                a target angle per gate of :math:`\pi/2`.
            repetitions (List[int]): By default the repetitions take on odd numbers for
                :math:`\pi/2` target angles as this ideally prepares states on the equator of
                the Bloch sphere. Note that the repetitions include two repetitions which
                plays the same role as including a circuit with an X gate.
            target_angle (float): The target angle per gate.
        """
        options = super()._default_experiment_options()
        options.add_sx = False
        options.add_xp_circuit = False
        options.repetitions = [1, 2, 3, 5, 7, 9, 11, 13, 15, 17, 21, 23, 25]
        options.target_angle = np.pi / 2
        return options

    @classmethod
    def _default_transpile_options(cls):
        """Default transpile options.

        Transpile Options:
            basis_gates (list(str)): A list of basis gates needed for this experiment.
                The schedules for these basis gates will be provided by the instruction
                schedule map from the calibrations.
        """
        options = super()._default_transpile_options()
        options.basis_gates = ["x", "sx"]

        return options

    @classmethod
    def _default_analysis_options(cls) -> Options:
        """Default analysis options."""
        options = super()._default_analysis_options()
        options.angle_per_gate = np.pi / 2
        options.phase_offset = 0

        return options
