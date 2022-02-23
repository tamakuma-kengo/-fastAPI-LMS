# fast-api-lms
## 環境の作成
#### リポジトリのクローン
ローカル環境ににリポジトリをクローンします.  

    git clone https://github.com/68ymtlab/fast-api-lms.git


#### Docker Desktopのインストール
以下のリンクから`Docker Desktop` インストーラをインストールします.  

https://docs.docker.com/desktop/windows/release-notes/    

*※ バージョン`4.5`にて, WSL2が使用できない不具合を確認しています. それ以降のバージョンか, 動作確認済みの`4.3.2`を使用してください.*  


インストーラを起動し, 画面の指示に従ってインストールをしてください. 
インストールが終了したら, コマンドプロンプトを開き,

    docker-compose --version
    
を実行し, バージョンが表示されたらインストールは完了です.  

***出力例***

    docker-compose version 1.29.2, build 5becea4c


#### docker 環境のビルド
以下のコマンドを実行し, `clone`したディレクトリに移動します.

    cd クローンした場所/fast-api-lms

続いて, docker環境をビルドします.  

    docker-compose build

#### 必要ライブラリのインストール
バックエンドで使用するFastAPI関連のライブラリをインストールします.   
以下のコマンドを実行します.

    docker-compose run --entrypoinst "poetry install" backend
    
#### コンテナを立ち上げる. 
`Docker Desktop` 上の `Container → fast-api-lms → fast-api-lms_frontend_1 → Start` をクリックします.  

![image](https://user-images.githubusercontent.com/29095003/155274753-02d0ef78-a1ff-43aa-9184-42c75b8ff9c7.png)
    
#### データベースのマイグレーションを実行する
データベース上でテーブルの作成と, 初期データのインサートを行います.  
以下のコマンドを実行します. 

    docker-compose exec backend poetry run python -m api.migrate_db
  
#### フロントエンドのプロジェクト作成
フロントエンドとして使用する`Vue.js`のプロジェクトを作成します. 
`Docker Desktop` 上の `Container → fast-api-lms → fast-api-lms_frontend_1 → CLI` をクリックします.   

![image](https://user-images.githubusercontent.com/29095003/155274124-b12c7ec3-31b9-4e8c-9e8d-41f0f165ac7c.png)

新たに端末が立ち上がるので,

    cd my-application
    
でカレントディレクトリを変更し,  

    npm install
    
で必要なライブラリをインストールします.   
この状態, または次のコマンドでエラーが出る場合は, `npm audit fix`を実行してください. 

次に, 作成したプロジェクトを起動します. 以下のコマンドを実行します. 

    npm run serve
    
## 作成した環境の確認
#### FastAPIバックエンドの確認
ブラウザ上で http://localhost:8000/docs を開きます.  
下の様なページが表示されます.   

![image](https://user-images.githubusercontent.com/29095003/155275231-baab5717-d327-4657-925e-c23b175606fb.png)

#### Vue.jsフロントエンドの確認
ブラウザ上で http://localhost:8080/Login を開きます. 
ログインフォームが表示されます. 

#### データベースの確認
`Docker Desktop` 上の `Container → fast-api-lms → fast-api-lms_db_1 → CLI` をクリックします.   
新しく端末が立ち上がるので, 端末上で

    mysql
    use demo;
    show tables;
    
を実行し, テーブルの一覧が表示されることを確認します. 

## 2回目以降の環境の起動方法
`Docker Desktop` 上の `Container → fast-api-lms → Start`をクリックします.   
コンテナが立ち上がるので, `Container → fast-api-lms → fast-api-lms_db_1 → CLI` を実行し, 開いた端末上で

    mysql
    use demo;
    
を実行します. 
 `Container → fast-api-lms → fast-api-lms_frontend_1 → CLI` を実行し, 開いた端末上で
 
    cd my-application
    npm run serve
    
を実行します. 
http://localhost:8000/docs  
http://localhost:8080/Login
を開いて, 起動完了です. 
