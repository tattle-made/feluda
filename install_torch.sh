pip uninstall -y torchvision
pip uninstall -y torch
if [[ "$OSTYPE" == "darwin"* ]]; then
  pip install torch==1.1.0
  pip install torchvision==0.3.0
else
  pip install https://download.pytorch.org/whl/cpu/torch-1.1.0-cp36-cp36m-linux_x86_64.whl
  pip install https://download.pytorch.org/whl/cpu/torchvision-0.3.0-cp36-cp36m-linux_x86_64.whl
fi