import torch
import torch.nn as nn
import torchvision
from torchvision import transforms, datasets


#### INTERFACE ####
def batch_classify(image_location):
    images = datasets.ImageFolder(image_location, transform=image_transforms)
    image_tensor = torch.stack([image[0] for image in images])
    return model(image_tensor.cuda())


#### SETUP ####

image_transforms = transforms.Compose([transforms.Resize((512, 512)),transforms.ToTensor()])

class ScreenshotClassifier(nn.Module):
  def __init__(self):
    super(ScreenshotClassifier, self).__init__()

    # Group 1
    self.conv11 = nn.Conv2d(3,64,kernel_size = 3, stride = 1, padding = 1)
    self.relu12 = nn.ReLU()
    self.conv13 = nn.Conv2d(64,64,kernel_size = 3, stride = 1, padding = 1)
    self.relu14 = nn.ReLU()
    self.max_pool15 = nn.Conv2d(64, 64,kernel_size = 2, stride = 2, padding = 0)

    # Group 2
    self.conv21 = nn.Conv2d(64,128,kernel_size = 3, stride = 1, padding = 1)
    self.relu22 = nn.ReLU()
    self.conv23 = nn.Conv2d(128,128,kernel_size = 3, stride = 1, padding = 1)
    self.relu24 = nn.ReLU()
    self.max_pool25 = nn.Conv2d(128, 128,kernel_size = 2, stride = 2, padding = 0)

    # Group 3
    self.conv31 = nn.Conv2d(128,256,kernel_size = 3, stride = 1, padding = 1)
    self.relu32 = nn.ReLU()
    self.conv33 = nn.Conv2d(256,256,kernel_size = 3, stride = 1, padding = 1)
    self.relu34 = nn.ReLU()
    self.max_pool35 = nn.Conv2d(256, 256,kernel_size = 2, stride = 2, padding = 0)

    # Group 4
    self.conv41 = nn.Conv2d(256,512,kernel_size = 3, stride = 1, padding = 1)
    self.relu42 = nn.ReLU()
    self.conv43 = nn.Conv2d(512,512,kernel_size = 3, stride = 1, padding = 1)
    self.relu44 = nn.ReLU()
    self.max_pool45 = nn.Conv2d(512, 512,kernel_size = 2, stride = 2, padding = 0)

    # Group 5
    self.conv51 = nn.Conv2d(512,1024,kernel_size = 3, stride = 1, padding = 1)
    self.relu52 = nn.ReLU()
    self.conv53 = nn.Conv2d(1024,1024,kernel_size = 3, stride = 1, padding = 1)
    self.relu54 = nn.ReLU()
    self.upsample55 = nn.ConvTranspose2d(1024, 512, kernel_size = 2, stride = 2, padding = 0)

    # Group 6
    self.conv61 = nn.Conv2d(1024,512,kernel_size = 3, stride = 1, padding = 1)
    self.relu62 = nn.ReLU()
    self.conv63 = nn.Conv2d(512,512,kernel_size = 3, stride = 1, padding = 1)
    self.relu64 = nn.ReLU()
    self.upsample65 = nn.ConvTranspose2d(512, 256, kernel_size = 2, stride = 2, padding = 0)

    # Group 7
    self.conv71 = nn.Conv2d(512,256,kernel_size = 3, stride = 1, padding = 1)
    self.relu72 = nn.ReLU()
    self.conv73 = nn.Conv2d(256,256,kernel_size = 3, stride = 1, padding = 1)
    self.relu74 = nn.ReLU()
    self.upsample75 = nn.ConvTranspose2d(256, 128, kernel_size = 2, stride = 2, padding = 0)

    # Group 8
    self.conv81 = nn.Conv2d(256,128,kernel_size = 3, stride = 1, padding = 1)
    self.relu82 = nn.ReLU()
    self.conv83 = nn.Conv2d(128,128,kernel_size = 3, stride = 1, padding = 1)
    self.relu84 = nn.ReLU()
    self.upsample85 = nn.ConvTranspose2d(128, 64, kernel_size = 2, stride = 2, padding = 0)

    # Group 9
    self.conv91 = nn.Conv2d(128,64,kernel_size = 3, stride = 1, padding = 1)
    self.relu92 = nn.ReLU()
    self.conv93 = nn.Conv2d(64,64,kernel_size = 3, stride = 1, padding = 1)
    self.relu94 = nn.ReLU()
    self.conv95 = nn.Conv2d(64, 2, kernel_size = 1, stride = 1, padding = 0)

    self.final_layer = nn.Linear(512 * 512, 2)


  def forward(self, input):
    #Group 1
    conv11_out = self.conv11(input)
    relu12_out = self.relu12(conv11_out)
    conv13_out = self.conv13(relu12_out)
    relu14_out = self.relu14(conv13_out)
    maxp15_out = self.max_pool15(relu14_out)

    #Group 2
    conv21_out = self.conv21(maxp15_out)
    relu22_out = self.relu22(conv21_out)
    conv23_out = self.conv23(relu22_out)
    relu24_out = self.relu24(conv23_out)
    maxp25_out = self.max_pool25(relu24_out)

    #Group 3
    conv31_out = self.conv31(maxp25_out)
    relu32_out = self.relu32(conv31_out)
    conv33_out = self.conv33(relu32_out)
    relu34_out = self.relu34(conv33_out)
    maxp35_out = self.max_pool35(relu34_out)

    #Group 4
    conv41_out = self.conv41(maxp35_out)
    relu42_out = self.relu42(conv41_out)
    conv43_out = self.conv43(relu42_out)
    relu44_out = self.relu44(conv43_out)
    maxp45_out = self.max_pool45(relu44_out)

    #Group 5
    conv51_out = self.conv51(maxp45_out)
    relu52_out = self.relu52(conv51_out)
    conv53_out = self.conv53(relu52_out)
    relu54_out = self.relu54(conv53_out)
    upsample55_out = self.upsample55(relu54_out)

    #Group 6
    conv61_out = self.conv61(torch.cat((relu44_out, upsample55_out), 1))
    relu62_out = self.relu62(conv61_out)
    conv63_out = self.conv63(relu62_out)
    relu64_out = self.relu64(conv63_out)
    upsample65_out = self.upsample65(relu64_out)

    #Group 7
    conv71_out = self.conv71(torch.cat((relu34_out, upsample65_out), 1))
    relu72_out = self.relu72(conv71_out)
    conv73_out = self.conv73(relu72_out)
    relu74_out = self.relu74(conv73_out)
    upsample75_out = self.upsample75(relu74_out)

    #Group 8
    conv81_out = self.conv81(torch.cat((relu24_out, upsample75_out), 1))
    relu82_out = self.relu82(conv81_out)
    conv83_out = self.conv83(relu82_out)
    relu84_out = self.relu84(conv83_out)
    upsample85_out = self.upsample85(relu84_out)

    #Group 9
    conv91_out = self.conv91(torch.cat((relu14_out, upsample85_out), 1))
    relu92_out = self.relu92(conv91_out)
    conv93_out = self.conv93(relu92_out)
    relu94_out = self.relu94(conv93_out)

    final_out = self.conv95(relu94_out)

    final_out_flat = torch.flatten(final_out, start_dim=2)

    final_out2 = self.final_layer(final_out_flat)

    return final_out2

model = torch.load('screenshot_classifier.pt')
