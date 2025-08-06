import numpy as np
from base64 import b64encode

def inline_video(filename, width=None, height=None, mimetype=None):
    """
    Create an HTML tag with embedded base64 data to encode a video

    Parameters
    ----------
    filename: str
        Path to file
    width: str
        HTML width of video
    height: str
        HTML height of video
    mimetype: str
        Mime type for video.  If unspecified, infer from file path
    
    Returns
    -------
    html: str
        HTML for this video
    """
    bs = b64encode(open(filename, "rb").read()).decode()
    if not mimetype:
        mimetype = filename.split(".")[-1]
    wh = ""
    if width:
        wh = f'with="{width}"'
    if height:
        wh += f'height="{height}"'
    html = f'<video {wh} controls src="data:video/{mimetype};base64,{bs}"/>'
    return html


def inline_image(filename, width=None, height=None, mimetype=None):
    """
    Create an HTML tag with embedded base64 data to encode an image

    Parameters
    ----------
    filename: str
        Path to file
    width: str
        HTML width of image
    height: str
        HTML height of image
    mimetype: str
        Mime type for image.  If unspecified, infer from file path
    
    Returns
    -------
    html: str
        HTML for this image
    """
    bs = b64encode(open(filename, "rb").read()).decode()
    if not mimetype:
        mimetype = filename.split(".")[-1]
    wh = ""
    if width:
        wh = f'with="{width}"'
    if height:
        wh += f'height="{height}"'
    html = f'<img {wh} src="data:video/{mimetype};base64,{bs}">'
    return html

def inline_compressed_audio(y, sr, rescale=True):
    """
    Compress raw audio and pack it into an HTML tag

    Parameters
    ----------
    y: ndarray(N)
        Audio samples
    sr: int
        Sample rate
    rescale: bool
        If True, mean center and scale the audio to be in the range [-1, 1]
    """
    from tempfile import NamedTemporaryFile
    from scipy.io import wavfile
    from base64 import b64encode
    import subprocess
    if rescale:
        y -= np.mean(y)
        y /= np.max(np.abs(y))
    y_wav = np.array(y*32676, dtype=np.int16)
    m4a_bstr = ""
    with NamedTemporaryFile(suffix=".wav") as fp_wav:
        wavfile.write(fp_wav.name, sr, y_wav)
        with NamedTemporaryFile(suffix=".m4a") as fp_m4a:
            cmd = ["ffmpeg", "-y", "-i", fp_wav.name, fp_m4a.name]
            subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            fp_m4a.seek(0)
            m4a_bstr = b64encode(fp_m4a.read())
            m4a_bstr = m4a_bstr.decode()
            fp_m4a.close()
        fp_wav.close()
    return f'<audio controls src="data:audio/m4a;base64,{m4a_bstr}"/>'