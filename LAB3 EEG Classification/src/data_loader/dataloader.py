import torch
import numpy as np
from torch.utils.data import TensorDataset, DataLoader


def read_bci_data(args):
    """load raw data"""

    """set data_path"""
    S4b_train = np.load(args.data_path+'S4b_train.npz')
    X11b_train = np.load(args.data_path+'X11b_train.npz')
    S4b_test = np.load(args.data_path+'S4b_test.npz')
    X11b_test = np.load(args.data_path+'X11b_test.npz')

    train_data = np.concatenate((S4b_train['signal'], X11b_train['signal']), axis=0)
    train_label = np.concatenate((S4b_train['label'], X11b_train['label']), axis=0)
    test_data = np.concatenate((S4b_test['signal'], X11b_test['signal']), axis=0)
    test_label = np.concatenate((S4b_test['label'], X11b_test['label']), axis=0)


    train_label = train_label - 1
    test_label = test_label -1
    train_data = np.transpose(np.expand_dims(train_data, axis=1), (0, 1, 3, 2))
    test_data = np.transpose(np.expand_dims(test_data, axis=1), (0, 1, 3, 2))
   

    mask = np.where(np.isnan(train_data))
    train_data[mask] = np.nanmean(train_data)

    mask = np.where(np.isnan(test_data))
    test_data[mask] = np.nanmean(test_data)

    return train_data, train_label, test_data, test_label



def create_dataset(args, device, train_data, train_label, test_data, test_label):
    """turn data into dataset"""

    """ndarray to torch.tensor, put tensor on device"""
    train_data = torch.FloatTensor(train_data).to(device)
    train_label = torch.LongTensor(train_label).to(device)
    test_data = torch.FloatTensor(test_data).to(device)
    test_label = torch.LongTensor(test_label).to(device)

    """data to dataset"""
    train_dataset = TensorDataset(train_data, train_label)
    test_dataset = TensorDataset(test_data, test_label)

    "batch slicing, shuffle only training data"
    train_dataset = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    test_dataset = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=False)

    return train_dataset, test_dataset
