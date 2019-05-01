# -*- coding: utf-8 -*-
"""
Image F/S output module
"""
from __future__ import absolute_import

from abc import ABCMeta, abstractproperty
import os.path

from niftynet.io.image_sink_base import ImageSinkBase
import niftynet.io.misc_io as misc_io

class ImageWriterBase(ImageSinkBase):
    """
    Interface for image sinks with F/S output
    """

    __metaclass__ = ABCMeta

    def __init__(self,
                 reader,
                 name='image_writer_base'):
        super(ImageWriterBase, self).__init__(reader, name=name)

    @abstractproperty
    def output_path(self):
        """
        Output directory path
        """

        return

    @abstractproperty
    def postfix(self):
        """
        Filename stem suffix applied to output files.
        """

        return


class ImageWriter(ImageWriterBase):
    """
    F/S output image writer class
    """

    def __init__(self,
                 source,
                 interp_order,
                 output_path='.',
                 postfix='_niftynet_out'):
        """
        :param output_path: output directory
        :param postfix: filename postfix applied to images
        """

        super(ImageWriter, self).__init__(source, interp_order)

        self._output_path = os.path.abspath(output_path)
        self._postfix = postfix
        self.inferred_cleared = False

    @property
    def output_path(self):
        return self._output_path

    @property
    def postfix(self):
        return self._postfix

    def layer_op(self, image_data_out, image_id, image_data_in):
        image_data_out = self._invert_preprocessing(image_data_out)

        subject_name = self.source.get_subject_id(image_id)
        filename = "{}{}.nii.gz".format(subject_name, self.postfix)
        misc_io.save_data_array(self.output_path,
                                filename,
                                image_data_out,
                                image_data_in,
                                self.interp_order)
        self.log_inferred(subject_name, filename)

    def log_inferred(self, subject_name, filename):
        """
        This function writes out a csv of inferred files

        :param subject_name: subject name corresponding to output
        :param filename: filename of output
        :return:
        """
        inferred_csv = os.path.join(self.output_path, 'inferred.csv')
        if not self.inferred_cleared:
            if os.path.exists(inferred_csv):
                os.remove(inferred_csv)
            self.inferred_cleared = True
            if not os.path.exists(self.output_path):
                os.makedirs(self.output_path)
        with open(inferred_csv, 'a+') as csv_file:
            filename = os.path.join(self.output_path, filename)
            csv_file.write('{},{}\n'.format(subject_name, filename))

