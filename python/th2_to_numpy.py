import numpy as np 
from skimage import img_as_uint

def th2_to_numpy(histogram):
    """Convert TH2 histogram to numpy array

    :histogram: TH2 object
    :returns: numpy array

    """
    width = histogram.GetNbinsX()
    height = histogram.GetNbinsY()
    image = np.fromiter(
            (histogram.fArray[i]
                for i in range(histogram.fN)),
            dtype=np.uint16,
            count=histogram.fN)
    image_array = img_as_uint(image)
    image_array = np.reshape(image_array, (height + 2, width + 2))
    image_array = np.delete(image_array, (0, height + 1), 0)
    image_array = np.delete(image_array, (0, width + 1), 1)
    image_array = np.flipud(image_array)
    return image_array

def numpy_to_th2(array, name="image"):
    """Convert numpy array to TH2

    :histogram: array
    :returns: TH2

    """
    if len(array.shape) != 2:
        raise ValueError("array must be 2D.")
    height = array.shape[0]
    width = array.shape[1]
    histogram = ROOT.TH2D(name, name,
            width, 0, width,
            height, 0, height)
    with_rows = np.vstack((
        np.zeros((width, 1), dtype=array.dtype)),
        array,
        np.zeros((width, 1), dtype=array.dtype)))
    with_columns = np.hstack((
        np.zeros((height + 2, 1), dtype=array.dtype)),
        with_rows,
        np.zeros((height + 2, 1), dtype=array.dtype)))
    histogram.fArray[:histogram.fN] = with_columns
    histogram.SetEntries(height * width)
    return histogram
