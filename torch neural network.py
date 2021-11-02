#!/usr/bin/env python
# coding: utf-8

# In[1]:


import torch
#x = torch.Tensor([5,3])
#y = torch.Tensor([2,1])


# In[26]:


#print(x*y)


# In[27]:


#x = torch.zeros([2,5])
#print(x)


# In[28]:


#x.shape()


# In[29]:


#x.shape


# In[30]:


#y = torch.rand([2,5])


# In[31]:


#y


# In[32]:


#y= y.view([1,10])
#y


# In[33]:


#y= y.view([1,10])


# In[34]:


#y


# In[35]:


import torchvision
from torchvision import transforms, datasets


# In[36]:


train = datasets.MNIST("", train = True, download = True, 
                       transform = transforms.Compose([transforms.ToTensor()]))

test = datasets.MNIST("", train = False, download = True, 
                       transform = transforms.Compose([transforms.ToTensor()]))


# In[37]:


trainset = torch.utils.data.DataLoader(train, batch_size = 10, shuffle = True)
testset = torch.utils.data.DataLoader(test, batch_size = 10, shuffle = True)


# In[38]:


for data in trainset:
    print(data)
    break


# In[39]:


x,y = data[0][0], data[1][0]

print(y)


# In[40]:


import matplotlib.pyplot as plt


# In[41]:


#plt.imshow(data[0][0])
print(data[0][0].shape)


# In[42]:


plt.imshow(data[0][0].view(28,28))
plt.show()


# In[45]:


total = 0
counter_dict = {0:0,1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}

for data in trainset:
    Xs, ys = data
    for y in ys:
        counter_dict[int(y)] +=1
        total += 1

        
print(counter_dict)


# In[48]:


for i in counter_dict:
    print(f"{i}: {counter_dict[i]/total*100}")


# In[49]:


import torch.nn as nn


# In[50]:


import torch.nn.functional as F


# In[57]:


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 64)
        self.fc4 = nn.Linear(64, 10)
    
    def forward(self,x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)
        
        return F.log_softmax(x, dim = 1)


# In[58]:


net = Net()
print(net)


# In[59]:


X = torch.rand((28,28))


# In[66]:


X = X.view(-1,28*28)


# In[67]:


output = net(X)


# In[68]:


output


# In[69]:


import torch.optim as optim

optimizer = optim.Adam(net.parameters(), lr = 0.001)


# In[77]:


EPOCHS = 3

for epoch in range(EPOCHS):
    for data in trainset:
        #data is a batch of featuresets and lanels
        X, y = data
        net.zero_grad()
        output = net(X.view(-1,28*28))
        loss = F.nll_loss(output,y)    
        loss.backward()
        optimizer.step()
    
    print(loss)


# In[79]:


correct = 0
total = 0

with torch.no_grad():
    for data in trainset:
        X,y = data
        output = net(X.view(-1, 784))
        for idx, i in enumerate(output):
            if torch.argmax(i) == y[idx]:
                correct+=1
            total += 1
            
print("Accurancy:", round(correct/total,3))


# In[85]:


import matplotlib.pyplot as plt
plt.imshow(X[7].view(28,28))
plt.show()


# In[84]:


print(torch.argmax(net(X[7].view(-1,784))[0]))


# In[ ]:




