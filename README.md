# gmshにおける血管モデルのメッシュ作成について

[gmsh](https://gmsh.info/)

最新バージョンのドキュメントがあるかもしれないから各自チェックしてください  
4.10.5を使用中（随時アップグレード予定）

[公式ドキュメント](http://gmsh.info/dev/doc/texinfo/gmsh.pdf)
[開発ディレクトリ](https://gitlab.onelab.info/gmsh/gmsh)

- python経由でgmshを開いてるっぽいので、gmshを直接ダウンロードしなくてよい？
  - バージョンアップしたかったら以下のコマンドをたたけばいいっぽい  
    こうすれば勝手にバージョンアップされたgmshを見に行く

    ```sh
    pip install --upgrade gmsh
    ```

## tips

- 公式ドキュメントを読もう  
  なんか大体ドキュメントに書いてある気がする  

- 下記のスクリプトを入れ込めば、設定で二次元のメッシュの可視化を毎回 ON にする操作をしなくて良くなる

  ```sh
  gmsh.option.setNumber("Mesh.SurfaceFaces", 1)
  ```

- 下記のスクリプトを入れ込めば、マウスのホイールのズームの逆転が慣れ親しんだものになる

  ```sh
  gmsh.option.setNumber("General.MouseInvertZoom", 1)
  ```

- 出力をファイルに残したいなら  
  gmsh上でlogファイルを残す方法があるか調査中

  ```sh
  # powershell(windows)なら
  python .\aneurysm.py > .\aneurysm.txt 2>&1 
  # macなら
  # linuxなら
  ```

- メッシュの出力形式を変更できる
  - OpenFOAMのgmshToFoamを使用するためにはmsh2の形式で出力したものを使う必要がある

  ```sh
  # mshで出力
  gmsh.write("cylinder_open.msh")
  # msh2で出力
  gmsh.write("cylinder_open.msh2")
  # vtkで出力
  gmsh.write("cylinder_open.vtk")
  ```

- 2d_airfoil.pyに関してはこのサイトを見てくださいv

  - [参考にしたサイト](https://mtkbirdman.com/gmsh-v4-6-0-python-2dairfoil)

## 解決したい問題

- 層ごとの厚さがしっかりと反映されない問題
  
  <img src="./images/layer_error.png" width="500" alt="問題の画像">  

  **それぞれのd[i]の厚さをi番目の層の厚さとしているのではなく、i番目の層を元々の基準線からどれくらいの距離に取るかを設定している模様**

- 下記のスクリプトはどの段階で実行するのがいいの？

  ```sh
  gmsh.model.geo.synchronize()
  ```

- 面を定義したとき結局どっちが法線方向なの

  - 中身が空洞の一枚の皮のような円筒を考えたとき法線を定義する表面は内側、外側どっちか？
    - なんか外側からさらに外側に向かって法線ベクトルが描画される  
      多分普通にstlの法線を出力してるだけ  
      [法線を表示する方法](https://www.rccm.co.jp/icem/pukiwiki/index.php?2D%E3%83%A1%E3%83%83%E3%82%B7%E3%83%A5%E3%81%AE%E6%B3%95%E7%B7%9A%E6%96%B9%E5%90%91%E3%83%99%E3%82%AF%E3%83%88%E3%83%AB%E3%81%AE%E8%A1%A8%E7%A4%BA%28Gmsh%29)  
      <img src="./images/normal_vector.png" width="500" alt="法線画像">  

- 境界層(boundary layer)の層ごとの厚さの変数の方は list じゃダメで、numpy.ndarray でないとダメらしい  
そんなこともないらしい？  
**nとdの型が一致していれば大丈夫っぽい**  
**それぞれのd[i]の厚さをi番目の層の厚さとしているのではなく、i番目の層を元々の基準線からどれくらいの距離に取るかを設定している模様**


  ```sh
  e = gmsh.model.geo.extrudeBoundaryLayer(gmsh.model.getEntities(2), n, -d, True)
  ```

## markdownのtips
- markdownのリスト内の改行は文末に半角空白2ついれればOK  
  こうすればOK
- **アスタリスク2個で挟めば強調だよ**
