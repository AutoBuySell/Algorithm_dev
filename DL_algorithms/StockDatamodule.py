from lightning.pytorch.utilities.types import EVAL_DATALOADERS, TRAIN_DATALOADERS, STEP_OUTPUT
from torch.utils.data import DataLoader, random_split

class StockDataModule(pl.LightningDataModule):
    def __init__(self, batch_size: int = 32, data_dir:str = '../data', window_size:int = 512, step_size:int=20, prediction_length:int = 100) -> None:
        super().__init__()
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.window_size = window_size
        self.step_size = step_size
        self.prediction_length = prediction_length

    def setup(self, stage: str) -> None:
        if stage == 'fit' or 'test': # a stage argument. used to separate setup logic for trainer.{fit,validate,test,predict}
            train_test_ratio = 0.9
            train_val_ratio = 0.8
            
            # make train dataset
            train_dataset = SlidingWindowDataset(
                data_dir=self.data_dir,
                window_size= self.window_size,
                step_size= self.step_size,
                prediction_length= self.prediction_length
            )


            # split train val test dataset
            self.train_dataset, self.val_dataset, self.test_dataset = random_split(
                train_dataset, [train_test_ratio * train_val_ratio, train_test_ratio * (1 - train_val_ratio), 1 - train_test_ratio]
            )

    def train_dataloader(self) -> TRAIN_DATALOADERS:
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True)

    def val_dataloader(self) -> EVAL_DATALOADERS:
        return DataLoader(self.val_dataset, batch_size=self.batch_size)

    def test_dataloader(self) -> EVAL_DATALOADERS:
        return DataLoader(self.test_dataset, batch_size=self.batch_size)

    # def predict_dataloader(self) -> EVAL_DATALOADERS:
    #     return DataLoader(self.predict_dataset, batch_size=self.batch_size)