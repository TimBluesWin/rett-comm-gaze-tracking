This is a program developed as part of my bachelor thesis, in order for the patients with Rett Syndrome to communicate by gazing one of the two available Activities of Daily Living (ADL) in the screen. It is made using Dlib and OpenCV framework on top of Python programming language. The algorithm of the program itself is inspired from antoinelame's gaze tracking program. However, during the writing of my bachelor's thesis

All instructions here are assuming that you are using a Windows platform.

<h2>Preparation</h2>

<h3>1. Install CMake for Windows</h3>
One way to do this is to download Visual Studio Tools 2022. Make sure that you select "Desktop Development with C++".
<h3>2. Install Pythony</h3>
The latest Python should work.
<h3>3.Install requirements</h3> 
pip install -r requirements.txt
<h3>4. Download Dlib Python directly</h3>
I found out that installing the latest version of DLib directly using pip does not work, so I personally downloaded the DLib library directly from here:

https://pypi.org/project/dlib/#files

Then after the tar files are downloaded, I extracted the files, and inside the DLib files, execute the following commands:

python -m build --wheel
pip install dist/dlib-(version).whl - replace "(version)" with whatever version of DLib you're downloading.

<h2>Running the program</h2>

<p>This program is designed to run with the web application, so make sure you have cloned the project "rett-comm-web-application" on the same folder as this project. To run the program, simply type "python rett-comm.py". You can now control the mouse cursor using your eyes. </p>