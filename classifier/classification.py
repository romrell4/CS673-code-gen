import torch
import torch.nn as nn
import torchvision
from torchvision import transforms, datasets


#### INTERFACE ####
def batch_classify(image_location):
    images = datasets.ImageFolder(image_location, transform=image_transforms)
    image_tensor = torch.stack([image[0] for image in images])
    image_names = [name.split('/')[-1] for name, _ in images.imgs]
    scores = model(image_tensor.cuda()).tolist()
    return {name: score for name, score in zip(image_names, scores)}


#### SETUP ####

image_transforms = transforms.Compose([transforms.Resize((512, 512)),transforms.ToTensor()])

class ScreenshotClassifier(nn.Module):
    def __init__(self):
        super(ScreenshotClassifier, self).__init__()

        self.relu = nn.ReLU()
        self.conv1 = nn.Conv2d(3,96,kernel_size=11, stride=4, padding=0)
        self.pool1 = nn.MaxPool2d(kernel_size=3, stride=2, padding=0)
        self.conv2 = nn.Conv2d(96, 256, kernel_size=5, stride=1, padding=0)
        self.pool2 = nn.MaxPool2d(kernel_size=3, stride=2, padding=0)
        self.conv3 = nn.Conv2d(256, 384, kernel_size=3, stride=1, padding=0)
        self.conv4 = nn.Conv2d(384, 384, kernel_size=3, stride=1, padding=0)
        self.conv5 = nn.Conv2d(384, 256, kernel_size=3, stride=1, padding=0)
        self.pool5 = nn.MaxPool2d(kernel_size=3, stride=2, padding=0)
        self.fc6 = nn.Linear(25600, 1024)
        self.fc7 = nn.Linear(1024, 1024)
        self.fc8 = nn.Linear(1024, 2)

    def forward(self, input):
        # input.shape = [2, 3, 512, 512]

        # level 1
        prog = self.conv1(input)
        prog = self.relu(prog)
        prog = self.pool1(prog)
        prog = self.relu(prog)
        # prog.shape = [2, 96, 62, 62]

        # level 2
        prog = self.conv2(prog)
        prog = self.relu(prog)
        prog = self.pool2(prog)
        prog = self.relu(prog)
        # prog.shape = [2, 256, 28, 28]

        # level 3
        prog = self.conv3(prog)
        prog = self.relu(prog)
        # prog.shape = [2, 384, 26, 26]

        # level 4
        prog = self.conv4(prog)
        prog = self.relu(prog)
        # prog.shape = [2, 384, 24, 24]

        # level 5
        prog = self.conv5(prog)
        prog = self.relu(prog)
        prog = self.pool5(prog)
        prog = self.relu(prog)
        # prog.shape = [2, 256, 10, 10]

        prog = torch.flatten(prog, start_dim=1)
        # prog.shape = [2, 25600]

        # level 6 + 7 + 8
        prog = self.fc6(prog)
        prog = self.relu(prog)
        prog = self.fc7(prog)
        prog = self.relu(prog)
        output = self.fc8(prog)

        # print(output)  # FIXME use this to test outputs
        return output

try:
    model = torch.load('screenshot_classifier.pt')
except:
    print('Could not load screenshot classification model. Did you download screenshot_classifier.pt from Box?')
# print(batch_classify('data'))
