"""
Perform interactive semantic segmentation
"""
import numpy as np
from napari import Viewer, gui_qt
from skimage import data
from segmentify.semantic import fit, predict
import napari
import imageio
print(napari.__version__)



with gui_qt():

    # create an empty viewer
    viewer = Viewer()

    # read in sample data
    # TODO better place to store example
    nuclei = np.load("./examples/nuclei.npy")
    nuclei = np.transpose(nuclei, (1,2,0))
    nuclei  = nuclei[:,:,0]
    labels = np.zeros(nuclei.shape, dtype=int)

    viewer.add_image(nuclei, name='input')

    # add empty labels
    viewer.add_labels(labels, name='output')
    viewer.add_labels(labels, name='train')
    viewer.layers['train'].opacity = 0.9

    @viewer.bind_key('s')
    def segment(viewer):
        image = viewer.layers['input'].data
        labels = viewer.layers['train'].data

        clf = fit(image, labels)

        segmentation = predict(clf, image)
        segmentation = np.squeeze(segmentation)
        print(segmentation.shape)
        viewer.layers['output'].data = segmentation