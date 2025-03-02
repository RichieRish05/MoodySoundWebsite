from services.custom_model import MoodyConvNet
import torch


def load_model():
    model = MoodyConvNet()
    model.load_state_dict(torch.load('services/best_model_weights.pth', map_location=torch.device('cpu'))['model_state_dict'])
    model.eval()
    return model




__all__ = [load_model.__name__]
