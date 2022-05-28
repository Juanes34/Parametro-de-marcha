# -*- coding: utf-8 -*-
"""
@autor: Eng. Alexander Sierra, Assistant Professor
"""
from typing import List
import numpy as np
import logging
import btk


# ----- acquisition -----
def smartReader(filename) -> btk.btkAcquisition:
    """Function to read a c3d file with BTK.

    :param `filename`: path and filename of the c3d
    :type `filename`: str
    :return: btk Acquisition instance
    :rtype: btk.btkAcquisition
    """
    
    reader = btk.btkAcquisitionFileReader()
    reader.SetFilename(filename)
    reader.Update()
    acq = reader.GetOutput()
    return acq


def smartWriter(acq, filename) -> None:
    """Function to write a c3d file with BTK.

    :param `acq`: a btk Acquisition instance
    :type `acq`: btkAcquisition
    :param `filename`: path and filename of the c3d
    :type `filename`: str
    """

    writer = btk.btkAcquisitionFileWriter()
    writer.SetInput(acq)
    writer.SetFilename(str(filename))
    writer.Update()


def getMarkerNames(acq) -> list:
    """Function to show point's label on acquisition.

    :param `acq`: a btk acquisition instance
    :type `acq`: btkAcquisition
    :return `marker_names`: marker names
    :rtype: list
    """

    marker_names = list()
    for it in btk.Iterate(acq.GetPoints()):
        if it.GetType() == btk.btkPoint.Marker and it.GetLabel()[0] != "*":
            marker_names.append(it.GetLabel())
    return marker_names


def isGap(acq, markerLabel) -> bool:
    """ Helper function to check if is there a gap.

    :param `acq`: a btk acquisition instance
    :type `acq`: btkAcquisition
    :param `markerLabel`: marker's label
    :type `markerLabel`: str
    :return `markerLabel`: True if there is a gap on specific marker
    :rtype: bool
    """

    residual_values = acq.GetPoint(markerLabel).GetResiduals()
    if np.any(residual_values == -1.0):
        logging.warning("Gap found for marker (%s)" % markerLabel)
        return True
    else:
        return False


def findMarkerGap(acq) -> list:
    """Function to find markers with Gap in a list of markers.

    :param `acq`: btk acquisition instance
    :type `acq`: btkAcquisition
    :return gaps: list of markers with gaps
    """
    gaps = list()
    markerNames = getMarkerNames(acq)
    for marker in markerNames:
        if isGap(acq, marker):
            gaps.append(marker)
    return gaps


def smartAppendPoint(acq, label, values,
                     pointType=btk.btkPoint.Marker, desc="",
                     residuals=None) -> None:
    """Function to append a point into an acquisition object.

    :param `acq`: (btkAcquisition) btk Acquisition instance
    :param `label`: (str) point's label
    :param `values`: (ndarray(n, 3)) point's values
    :param `pointType`: (enums of btkPoint) type of Point
    :param `residuals`:
    :return: None
    """
    values = np.nan_to_num(values)

    if residuals is None:
        residuals = np.zeros((values.shape[0], 1))
        for i in np.arange(values.shape[0]):
            if np.all(values[i, :] == 0.0):
                residuals[i] = -1.0

    new_btkPoint = btk.btkPoint(label, acq.GetPointFrameNumber())
    new_btkPoint.SetValues(values)
    new_btkPoint.SetDescription(desc)
    new_btkPoint.SetType(pointType)
    new_btkPoint.SetResiduals(residuals)
    acq.AppendPoint(new_btkPoint)


def constructEmptyMarker(acq, label, desc="") -> None:
    """
    Function to build an empty marker.
    :param acq: (btkAcquisition) btk Acquisition instance
    :param label: (str) marker's label
    :param desc: (str) "short description"
    :return: None
    """
    nFrames = acq.GetPointFrameNumber()
    values = np.zeros((nFrames, 3))
    residualValues = np.full((nFrames, 1), -1.0)
    smartAppendPoint(acq, label, values, desc=desc, residuals=residualValues)
    logging.debug("built " + label)


# ----- Angles -----

def getAngleNames(acq) -> list:
    """Function to show angle's label on acquisition.

    :param `acq`: a btk acquisition instance
    :type `acq`: btkAcquisition
    :return `marker_names`: marker names
    :rtype: list
    """

    angle_names = list()
    for it in btk.Iterate(acq.GetPoints()):
        if it.GetType() == btk.btkPoint.Angle:
            angle_names.append(it.GetLabel())
    return angle_names

# ----- Events -----

def _GetEvents(acq):
    """
    Helper function to read and sort the event collection from an acq object
    :param acq: (btkAcquisition)
    :return: (list) List of btkEvent objects
    """
    event_list = [event for event in btk.Iterate(acq.GetEvents())]
    event_list.sort(key=lambda i:i.GetFrame())
    return  event_list

def get_events(acq, context):
    """
    Function to read the event's frame by context
    :param acq: (btkAcquisition) btk Acquisition instance
    :param context: (string) 'Right', 'Left' or 'General'
    :return: (tuple) Foot Strike list and Foot Off list
    """
    footStrike = []
    footOff =  []

    for e in _GetEvents(acq):
        if e.GetContext() == context:
            if e.GetLabel() == 'Foot Strike':
                footStrike.append(e.GetFrame())
            if e.GetLabel() == 'Foot Off':
                footOff.append(e.GetFrame())
    return (footStrike, footOff)
