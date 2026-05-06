import mlflow
import mlflow.sklearn
import pandas as pd
import yaml
import json
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

EVAL_THRESHOLD = 0.60


def train(
    params: dict,
    data_path: str = "data/train_phase1.csv",
    eval_path: str = "data/eval.csv",
) -> float:
    """
    Huan luyen mo hinh va ghi nhan ket qua vao MLflow.

    Tham so:
        params     : dict chua cac sieu tham so cho RandomForestClassifier.
        data_path  : duong dan den file du lieu huan luyen.
        eval_path  : duong dan den file du lieu danh gia.

    Tra ve:
        accuracy (float): do chinh xac tren tap danh gia.
    """

    # 1. Doc du lieu huan luyen va danh gia
    df_train = pd.read_csv(data_path)
    df_eval  = pd.read_csv(eval_path)

    # 2. Tach dac trung (X) va nhan (y)
    X_train = df_train.drop(columns=["target"])
    y_train = df_train["target"]
    X_eval  = df_eval.drop(columns=["target"])
    y_eval  = df_eval["target"]

    # --- THEM BUOC SCALING DE CAI THIEN DO CHINH XAC ---
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_eval  = scaler.transform(X_eval)
    # --------------------------------------------------

    with mlflow.start_run():

        # 3. Ghi nhan cac sieu tham so
        mlflow.log_params(params)

        # 4. Khoi tao va huan luyen RandomForestClassifier
        model = RandomForestClassifier(
            n_estimators=params.get("n_estimators", 100),
            max_depth=params.get("max_depth", None),
            min_samples_split=params.get("min_samples_split", 2),
            random_state=42
        )
        model.fit(X_train, y_train)

        # Luu luon scaler vao model folder de dung luc serve
        os.makedirs("models", exist_ok=True)
        joblib.dump(scaler, "models/scaler.pkl")

        # 5. Du doan tren tap danh gia va tinh chi so
        preds = model.predict(X_eval)
        acc   = accuracy_score(y_eval, preds)
        f1    = f1_score(y_eval, preds, average="weighted")

        # 6. Ghi nhan chi so vao MLflow
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)
        mlflow.sklearn.log_model(model, "model")

        # 7. In ket qua ra man hinh
        print(f"Accuracy: {acc:.4f} | F1: {f1:.4f}")

        # 8. Luu metrics ra file outputs/metrics.json
        os.makedirs("outputs", exist_ok=True)
        with open("outputs/metrics.json", "w") as f:
            json.dump({"accuracy": acc, "f1_score": f1}, f)

        # 9. Luu mo hinh ra file models/model.pkl
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/model.pkl")

    return acc


if __name__ == "__main__":
    with open("params.yaml") as f:
        params = yaml.safe_load(f)
    train(params)
