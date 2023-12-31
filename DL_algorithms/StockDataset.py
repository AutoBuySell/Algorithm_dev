import pandas as pd
from torch.utils.data import Dataset
import torch

class SlidingWindowDataset(Dataset):
    def __init__(self, data_path, window_size=512, step_size=20, prediction_length=100):
        self.window_size = window_size
        self.step_size = step_size
        self.prediction_length = prediction_length
        self.data = pd.read_csv(data_path)

        self.processed_data, self.labels = self._preprocess()

    def _preprocess(self):
        processed_data = []
        labels = []
        
        for start in range(0, len(self.data) - self.window_size - self.prediction_length, self.step_size):
            end = start + self.window_size
            window_data = self.data[start:end]['o']
            label_data = self.data[end:end + self.prediction_length]['o'].mean()

            # window_data의 마지막 데이터를 기준으로 스케일링
            scaling_factor = window_data.iloc[-1]  # 마지막 가격을 스케일링 팩터로 사용
            scaled_window_data = window_data / scaling_factor        
            scaled_label_data = label_data / scaling_factor

            processed_data.append(scaled_window_data)
            labels.append(scaled_label_data)

        return processed_data, labels

    def __len__(self):
        return len(self.processed_data)

    def __getitem__(self, idx):
        data = self.processed_data[idx].to_numpy() # pandas.Series는 바로 tensor로 안되고 numpy를 거쳐야 변환됨.
        label = self.labels[idx]
        return torch.tensor(data, dtype=torch.float32), torch.tensor(label, dtype=torch.float32)
        
        