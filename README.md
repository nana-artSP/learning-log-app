# 学習ログ管理アプリ

## 🔗 公開URL
https://learning-log-app-ae2i.onrender.com/login

---

## 概要
日々の学習時間を記録・管理するために作成したWebアプリです。  
学習の継続を可視化し、モチベーション維持につなげることを目的としています。  

ログイン後に、学習ログの追加・一覧表示・編集・削除が可能です。  
また、開始時刻と終了時刻を利用したタイムカード風の記録にも対応しています。

---

## 使用技術
- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Bootstrap

---

## 機能一覧
- ログイン機能
- 学習ログの追加
- 学習ログの一覧表示
- 学習ログの編集
- 学習ログの削除
- 学習時間の自動計算
- 開始時刻 / 終了時刻の記録

---

## 工夫した点
- Flaskで画面とAPIを統一し、シンプルな構成にした点
- 学習開始・終了時刻から学習時間を自動計算できるようにした点
- Bootstrapを使用し、見やすくシンプルなUIを意識した点
- 入力補助（プルダウン・日付自動入力）を実装し、操作性を向上させた点

---

## 画面イメージ

### ログイン画面
<img width="1128" height="903" alt="image" src="https://github.com/user-attachments/assets/d799eba0-293b-41dd-aa3b-da18e6a0e6c9" />


### 学習ログ一覧
<img width="1295" height="259" alt="image" src="https://github.com/user-attachments/assets/1b5d1322-8792-45df-bcf8-ec6f0230ab6c" />


### 編集画面
<img width="1296" height="598" alt="image" src="https://github.com/user-attachments/assets/f46affc0-8fea-4f2f-8c8c-6f673c0e1517" />

### 学習ログ追加
<img width="1317" height="706" alt="image" src="https://github.com/user-attachments/assets/18867c30-441a-4953-bf3f-c2c0a83d21a3" />



---

## 注意事項
- 初回利用時はユーザー登録が必要です  
- 以下から登録できます  

👉 https://learning-log-app-ae2i.onrender.com/signup_page  

※ 無料環境のため、データがリセットされる場合があります

---

## ローカルでの起動方法

```bash
python app.py
