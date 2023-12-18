from lightning.pytorch.utilities.types import EVAL_DATALOADERS, TRAIN_DATALOADERS, STEP_OUTPUT
from torch.utils.data import DataLoader, random_split
import pytorch_lightning as pl
from torch.utils.data import Subset
from StockDataset import SlidingWindowDataset

class StockDataModule(pl.LightningDataModule):
    def __init__(self, data_path, batch_size: int = 32, window_size:int = 512, step_size:int=20, prediction_length:int = 100) -> None:
        super().__init__()
        self.data_path = data_path
        self.batch_size = batch_size
        self.window_size = window_size
        self.step_size = step_size
        self.prediction_length = prediction_length

    def setup(self, stage: str) -> None:
        if stage == 'fit': # a stage argument. used to separate setup logic for trainer.{fit,validate,test,predict}
            train_ratio = 0.8

            
            # make train dataset
            train_dataset = SlidingWindowDataset(
                data_path=self.data_path,
                window_size= self.window_size,
                step_size= self.step_size,
                prediction_length= self.prediction_length
            )

            dataset_length = len(train_dataset)
            train_size = int(dataset_length * train_ratio)

            # split train val test dataset
            # random_split은 Subset를 random으로 반환. 
            # random이 아니라 고정된 Subset반환
            # Subset(데이터, 인덱스) -> 데이터를 인덱스기준으로 나눔.
            self.train_dataset = Subset(train_dataset, range(0, train_size))
            self.val_dataset = Subset(train_dataset, range(train_size, dataset_length))

    def train_dataloader(self) -> TRAIN_DATALOADERS:
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True)

    def val_dataloader(self) -> EVAL_DATALOADERS:
        return DataLoader(self.val_dataset, batch_size=self.batch_size)

    # def test_dataloader(self) -> EVAL_DATALOADERS:
    #     return DataLoader(self.test_dataset, batch_size=self.batch_size)

    # def predict_dataloader(self) -> EVAL_DATALOADERS:
    #     return DataLoader(self.predict_dataset, batch_size=self.batch_size)