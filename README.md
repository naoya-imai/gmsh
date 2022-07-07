# 公式ドキュメントをしっかり読もう

なんか大体ドキュメントに書いてある気がする
最新バージョンのドキュメントがあるかもしれないから各自チェックしてくれ

http://gmsh.info/dev/doc/texinfo/gmsh.pdf

# tips

- 下記のスクリプトを入れ込めば、設定で二次元のメッシュの可視化を毎回ONにする操作をしなくて良くなる

  ```sh
  gmsh.option.setNumber("Mesh.SurfaceFaces", 1)
  ```

- 下記のスクリプトを入れ込めば、マウスのホイールのズームの逆転が慣れ親しんだものになる

  ```sh
  gmsh.option.setNumber("General.MouseInvertZoom", 1)
  ```

# 解決したい疑問

- 下記のスクリプトはどの段階で実行するのがいいの？

  ```sh
  gmsh.model.geo.synchronize()
  ```