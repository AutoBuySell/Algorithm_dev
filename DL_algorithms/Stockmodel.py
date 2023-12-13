import torch
import torch.nn.functional as F

class Stock_LSTM(pl.LightningModule):
    def __init__(self, input_dim, hidden_dim, output_dim, seq_length, LSTM_layers,dropout):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers=LSTM_layers, bidirectional=False, dropout=dropout)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim, output_dim)

        self.training_step_outputs = []
        self.validation_step_outputs = []

    def forward(self, x):
        x, _ = self.lstm(x)
        x = x.reshape(x.size(0), -1)
        x = self.fc(x)
        return x
    
    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.mse_loss(y_hat, y)

        metrics = {
            'train_loss': loss, #정확도는 뺐음. 이후 코드도 정확도는 제외
        }
        self.training_step_outputs.append(metrics)
        self.log_dict(metrics, prog_bar=True)

        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.mse_loss(y_hat, y)

        metrics = {
            'val_loss': loss,
        }
        self.validation_step_outputs.append(metrics)
        self.log_dict(metrics, prog_bar=True)
        return loss
    
    def on_validation_epoch_end(self):
        if not (self.training_step_outputs and self.validation_step_outputs):
            return

        train_avg_loss = torch.stack([x["train_loss"]
            for x in self.training_step_outputs]).mean()
        metrics = {
            "train_avg_loss": train_avg_loss
        }
        self.log_dict(metrics)

        val_avg_loss = torch.stack([x["val_loss"]
            for x in self.validation_step_outputs]).mean()
        metrics = {
            "val_avg_loss": val_avg_loss
        }
        self.log_dict(metrics)

        print("\n" +
              (f'Epoch {self.current_epoch}, Avg. Training Loss: {train_avg_loss:.3f}' +
               f'Avg. Validation Loss: {val_avg_loss:.3f}'), flush=True)

        self.training_step_outputs.clear() # 초기화
        self.validation_step_outputs.clear()

    def test_step(self, batch, batch_idx):
        x, y = batch

        y_hat = self(x)
        loss = F.mse_loss(y_hat, y)

        metrics = {
            'test_loss': loss,
        }
        self.log_dict(metrics, prog_bar=True)

    def predict_step(self, batch, batch_idx):
        return torch.argmax(self.model(batch), dim=-1)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.001)