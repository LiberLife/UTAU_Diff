# UTAU_DIFF

UTAU プラグイン。取得済みの Snapshot と、選択されたデータを比較する。
具体的には下記のことができる。

1. 選択されたデータの Snapshot を取得する
2. 取得済みの Snapshot と選択されたデータを比較する
3. 選択されたデータを取得済みの Snapshot に切り戻す


## 必要なツール

本ツールは、データの比較に [WinMerge](https://winmerge.org/?lang=ja) の利用を想定している。本ツールの中に `WinMerge` は含まれていないため、別途ダウンロードが必要。

ただし、コマンドプロンプトから2つのファイルを渡して、差分を表示できるアプリケーションであれば、他のものでも問題ない。



## 利用方法

1. `diff.zip` を解凍して、すべてのファイルを UTAU のプラグイン用ディレクトリに配置する。

    - ただし、`diff.zip` は、ヴォ―ジョンアップの度に、 Python ファイルを 実行ファイル化し、さらに圧縮するという作業を行っているため、たまにソースコードよりも古い内容のままのことがあるかもしれないので、要注意
    - 本ツールの exe 化には、 `PyInstaller` を利用している

2. `settings.ini` ファイルを開き、 `app` セクションの `win_merge_file` パラメータに、 `WinMerge` のパスを指定する。文字コードは **UTF-8** 、改行コードは **LF** で。

2. UTAU 本体を起動して、対象となるノートを選択し、 `ツール` > `プラグイン` > `Diff` を選択する。

3. コマンドプロンプトが立ち上がると、下記のように、現在取得済の Snapshot の一覧が表示され、何を実行するか、選択待ち状態となる。

    - スナップショットは最大16取得でき、取得中のスナップショットは、インデックス 00 ~ 15 のうち、タイムスタンプが表示されているもの
    - インデックスの次に表示されているアルファベットは、現在のデータとスナップショットの**簡易的な一致情報**
    - アルファベットの意味は下記の通り
        - C: 現在選択中のノート数とスナップショットのノート数が同じ。ここが異なっている場合、他の項目は比較しない
        - l: 現在選択中のノートとスナップショットのノートの長さがすべて一致する。UTAU
         のエントリ名は、 `Length`
        - y: 歌詞がすべて一致する。エントリ名は、 `Lyric`
        - n: 音の高さがすべて一致する。エントリ名は、 `NoteNum`
        - p: 先行発声がすべて一致する。エントリ名は、 `PreUtterance`
    - 一致情報の次は、スナップショットを取得したときのタイムスタンプ
    - 次は、スナップショット名
    - 最後にメッセージ。ない場合もある

```cmd
Use Ctrl-Z plus Return to quit.
Snapshots:
  00 Clyn- 2019-10-22 22:46:19 Rap
  01 Cly-p 2019-10-22 22:47:24 Vel2Int Test_Message
  02 -----
  03 -----
  04 -----
  05 -----
  06 -----
  07 -----
  08 -----
  09 -----
  10 -----
  11 -----
  12 -----
  13 -----
  14 -----
  15 -----

What do you do?
  0. Snap data
  1. Show diff
  2. Remove a snapshot
  3. Remove all snapshots
  4. Failback
Select index(0~4)[0]:
```

4. 実行する選択肢は下記の通り。

    - 0. Snap data: スナップショットを取得する
    - 1. Show diff: `WinMerge` を利用し、選択中のデータとスナップショットを比較する
    - 2. Remove a snapshot: 取得済みの Snapshot を削除する
    - 3. Remove all snapshots: 取得済みの全ての Snapshot を削除する
    - 4. Failback: 選択中のデータを、指定の Snapshot に切り戻す



## .py ファイルの .exe ファイル化手順

本ツールを作成後、配布用に exe ファイル化する場合は、下記の手順を実行する。

1. 本ツールのルートに `diff.spec` ファイルを作成する。

```diff.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['app\\diff.py'],
             pathex=['.\\'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='diff',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )

import shutil

shutil.copyfile('app\\settings.ini', '{0}\\settings.ini'.format(DISTPATH))
shutil.copyfile('app\\plugin.txt', '{0}\\plugin.txt'.format(DISTPATH))
```

2. `pyinstller` コマンドを実行する。

    - `pyinstaller` は、別途インストールされていることが必要

```cmd
pyinstaller diff.spec --clean
```



## 問題点など

### UTAU のバグ

下記の事象については、 UTAU のバグの可能性がある。

- `[#PREV]` および `[#NEXT]` セクションが存在しない全ノートを対象とする切り戻しの場合、全てのノートを `[#DELETE]` し、新たなノートを `[#INSERT]` すると、元データの最後のノートが残る

なお、この点については、 [UTAU_batDeTest
](https://github.com/LiberLife/UTAU_batDeTest) を利用した手動による書き換えでも、同じ事象が発生することを確認している。

具体的には下記のようなデータ（読み込み専用データなど、一部省略）。

スナップショットデータ。歌詞は「あいう」。

```00.txt
[#VERSION]
UST Version 1.20
[#SETTING]
Tempo=120.00
[#0000]
Length=960
Lyric=あ
NoteNum=66
Intensity=50
Modulation=0
[#0001]
Length=900
Lyric=い
NoteNum=68
Intensity=50
Modulation=0
[#0002]
Length=540
Lyric=う
NoteNum=70
Intensity=50
Modulation=0
```

現在のデータ。歌詞は「かき」

```tmp2BE7.tmp
[#VERSION]
UST Version 1.20
[#SETTING]
Tempo=120.00
[#0000]
Length=960
Lyric=か
NoteNum=66
Intensity=50
Modulation=0
[#0001]
Length=540
Lyric=き
NoteNum=70
Intensity=50
Modulation=0
```

現在のデータを、スナップショットのデータに切り戻すために、現在のデータを次のように整形する。歌詞「かき」部分の2つのノートを削除し、歌詞「あいう」部分を挿入する想定。

```
[#VERSION]
UST Version 1.20
[#SETTING]
Tempo=120.00
[#DELETE]
[#DELETE]
[#INSERT]
Length=960
Lyric=あ
NoteNum=66
Intensity=50
Modulation=0
[#INSERT]
Length=900
Lyric=い
NoteNum=68
Intensity=50
Modulation=0
[#INSERT]
Length=540
Lyric=う
NoteNum=70
Intensity=50
Modulation=0
```

実行結果は、歌詞「あいうき」で、なぜか、歌詞「き」のノートが残る。

なお、前後に音符があるような場合、つまり `[#PREV]` および `[#NEXT]` セクションがあるような、部分データの切り戻しの場合、このような不具合は起こらない。


### エントリ PreUtterance について

先行発声を示すエントリ `PreUtterance` について、[UTAU ユーザー互助会@ ウィキ](https://w.atwiki.jp/utaou/pages/64.html)では、以下のように記されている。

>PreUtterance　先行発声  
>書式 : PreUtterance=実数  
>定義域 : 60000未満  
>単位 : ミリ秒  
>デフォルト値 : 空白(原音値)  
>エントリ自体は必ず存在しますが、値が空白の事があります。  

実際には、ノート入力直後や、インポート直後などには、ほとんどの場合 `PreUtterance` は存在しない。 `PreUtterance` が現れる契機は不詳。旧ヴァージョンなどでは、必ず存在したのかもしれない。


## ヴァージョン

0.0.1 (2019-10-23)


