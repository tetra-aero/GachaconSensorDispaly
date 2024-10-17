// server.js
const express = require('express');
const cors = require('cors')
const morgan = require('morgan');
const path = require('path');
const app = express();

const port = 3000;

// メモリ上にログを保持する配列
let logMemory = [];
const MAX_LOGS = 100; // ログの最大件数

app.use(cors())

// morganのカスタムフォーマットで、/logs へのアクセスを除外してログをメモリに保存
app.use((req, res, next) => {
  if (req.path !== '/logs' && req.path !== '/logs-page') {  // /logs エンドポイントを除外
    morgan('combined', {
      stream: {
        write: (message) => {
          logMemory.push(message.trim()); // ログをメモリに追加

          // ログがMAX_LOGS件を超えたら古いログを削除
          if (logMemory.length > MAX_LOGS) {
            logMemory.shift(); // 最も古いログを削除
          }
        }
      }
    })(req, res, next);
  } else {
    next();
  }
});



// ランダムな整数を生成する関数
function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// 30個のオブジェクトを生成し、ランダムな値を返す関数
function generateSineWaveData() {
    const titles =['Title_1', 'Title_2', 'Title_3', 'Title_4', 'Title_5', 'Title_6', 'Title_7', 'Title_8', 'Title_9', 'Title_10', 'Title_11', 'Title_12', 'Title_13', 'Title_14', 'Title_15', 'Title_16', 'Title_17', 'Title_18', 'Title_19', 'Title_20', 'Title_21', 'Title_22', 'Title_23', 'Title_24', 'Title_25', 'Title_26', 'Title_27', 'Title_28', 'Title_29', 'Title_30']
    ;
    const units = ['V', 'm', 'mA', 'W/s', 'Hz', 'A', 'g', 'm/s', 'hPa'];
    
    const data = [];
    //const amplitude = 5000;  // サイン波の振幅
    const frequency = 0.2;   // 周波数
    const offset = 5000;     // オフセット（中心の高さ）
    
    for (let i = 0; i < 30; i++) {
        const randomTitle = titles[i % titles.length]; // タイトルは循環
        const randomData = getRandomInt(1000, 9999); // 1000～9999のランダムな数値
        const randomUnit = units[i % units.length]; // 単位は循環
        //console.log(randomData)
        const sineValue = Math.sin(i * frequency) * randomData + randomData;

        data.push({
            title: randomTitle,
            data:  Math.round(sineValue).toString(), // 数値を文字列に変換
            unit: randomUnit
        });
    }
    
    return data;
}

// APIエンドポイント
app.get('/api/data', (req, res) => {
  console.log("Accessed")
    const sineWaveData  = generateSineWaveData();
    res.json(sineWaveData);
});
// ログ確認用のページ (HTMLファイルを提供)
app.get('/logs-page', (req, res) => {
  res.sendFile(path.join(__dirname, 'log.html'));
});
// ログを確認するエンドポイント
app.get('/logs', (req, res) => {
  res.json(logMemory); // メモリ上のログをJSONとして返す
});
// ログ消去のエンドポイント［DELETEメソッド］
app.delete('/logs', (req, res) => {
  logMemory = []; // メモリ上のログを全て削除
  res.json({ message: 'ログが削除されました' }); // 確認メッセージを返す
});

// サーバーの起動
app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});