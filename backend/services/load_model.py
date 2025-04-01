from services.custom_model import MoodyConvNet
import torch
import boto3
import os

def load_model(weights_path):
    model = MoodyConvNet()
    model.load_state_dict(torch.load(weights_path, map_location=torch.device('cpu'))['model_state_dict'])
    model.eval()
    return model

def download_weights():
    s3 = boto3.client('s3')
    s3.download_file(
        Bucket=os.getenv('WEIGHTS_BUCKET_NAME'),
        Key='ray_results/NormalizedMoodyConvNet/best_model.pth',
        Filename='services/best_model_weights.pth'
    )



__all__ = [load_model.__name__, download_weights.__name__]
