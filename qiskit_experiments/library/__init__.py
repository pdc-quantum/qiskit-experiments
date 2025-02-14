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

"""
======================================================
Experiment Library (:mod:`qiskit_experiments.library`)
======================================================

.. currentmodule:: qiskit_experiments.library

A library of of quantum characterization, calibration and verification
experiments for calibrating and benchmarking quantum devices. See
:mod:`qiskit_experiments.framework` for general information the framework
for running experiments.


.. _verification:

Verification Experiments
========================

Experiments for verification and validation of quantum devices.

.. autosummary::
    :toctree: ../stubs/
    :template: autosummary/experiment.rst

    ~randomized_benchmarking.StandardRB
    ~randomized_benchmarking.InterleavedRB
    ~tomography.StateTomography
    ~tomography.ProcessTomography

.. autosummary::
    :toctree: ../stubs/

    ~quantum_volume.QuantumVolume

.. _characterization:

Characterization Experiments
============================

Experiments for characterization of qubits and quantum device properties.
Some experiments may be also used for gate calibration.

.. autosummary::
    :toctree: ../stubs/
    :template: autosummary/experiment.rst

    ~characterization.T1
    ~characterization.T2Ramsey
    ~characterization.QubitSpectroscopy
    ~characterization.EFSpectroscopy
    ~characterization.CrossResonanceHamiltonian
    ~characterization.EchoedCrossResonanceHamiltonian
    ~characterization.FineAmplitude
    ~characterization.FineXAmplitude
    ~characterization.FineSXAmplitude

.. _calibration:

Calibration Experiments
=======================

Experiments for pulse level calibration of quantum gates. These experiments
are usually run with a
:py:class:`~qiskit_experiments.calibration_management.Calibrations`
class instance to manage parameters and pulse schedules.
See :doc:`/tutorials/calibrating_armonk` for example.

.. autosummary::
    :toctree: ../stubs/
    :template: autosummary/experiment.rst

    ~calibration.RoughFrequencyCal
    ~calibration.DragCal
    ~calibration.FineDrag
    ~calibration.FineXDrag
    ~calibration.FineSXDrag
    ~calibration.Rabi
    ~calibration.EFRabi
    ~calibration.FineAmplitudeCal
    ~calibration.FineXAmplitudeCal
    ~calibration.FineSXAmplitudeCal
    ~calibration.RamseyXY

"""
from .calibration import (
    DragCal,
    FineDrag,
    FineXDrag,
    FineSXDrag,
    Rabi,
    EFRabi,
    FineAmplitudeCal,
    FineXAmplitudeCal,
    FineSXAmplitudeCal,
    RoughFrequencyCal,
    RamseyXY,
)
from .characterization import (
    T1,
    T2Ramsey,
    QubitSpectroscopy,
    EFSpectroscopy,
    CrossResonanceHamiltonian,
    EchoedCrossResonanceHamiltonian,
    FineAmplitude,
    FineXAmplitude,
    FineSXAmplitude,
)
from .randomized_benchmarking import StandardRB, InterleavedRB
from .tomography import StateTomography, ProcessTomography
from .quantum_volume import QuantumVolume

# Experiment Sub-modules
from . import calibration
from . import characterization
from . import randomized_benchmarking
from . import tomography
from . import quantum_volume
