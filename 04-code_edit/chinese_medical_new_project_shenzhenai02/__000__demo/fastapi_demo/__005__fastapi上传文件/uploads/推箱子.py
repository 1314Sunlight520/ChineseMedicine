from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <!DOCTYPE html>
    <html lang=\"zh-CN\">
    <head>
      <meta charset=\"utf-8\" />
      <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
      <title>推箱子 - FastAPI 内嵌版</title>
      <style>
        :root {
          --bg: #0f172a;       /* slate-900 */
          --panel: #111827;    /* gray-900 */
          --text: #e5e7eb;     /* gray-200 */
          --muted: #9ca3af;    /* gray-400 */
          --accent: #22c55e;   /* green-500 */
          --accent-2: #60a5fa; /* blue-400 */
          --wall: #475569;     /* slate-600 */
          --floor: #1f2937;    /* gray-800 */
          --target: #fbbf24;   /* amber-400 */
          --box: #f97316;      /* orange-500 */
          --box-ok: #10b981;   /* emerald-500 */
          --player: #60a5fa;   /* blue-400 */
        }
        * { box-sizing: border-box; }
        body {
          margin: 0; padding: 0; background: var(--bg); color: var(--text);
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji', sans-serif;
          display: flex; align-items: center; justify-content: center; min-height: 100vh;
        }
        .wrap { width: 100%; max-width: 900px; padding: 24px; }
        .card { background: var(--panel); border: 1px solid #1f2937; border-radius: 12px; padding: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
        .title { display:flex; align-items:center; justify-content:space-between; margin-bottom: 12px; }
        h1 { font-size: 20px; margin: 0; }
        .muted { color: var(--muted); font-size: 12px; }
        .toolbar { display:flex; gap:8px; flex-wrap: wrap; }
        button { background: #1f2937; color: var(--text); border: 1px solid #374151; border-radius: 8px; padding: 8px 12px; cursor: pointer; }
        button:hover { border-color: #4b5563; }
        button:active { transform: translateY(1px); }
        .info { display:flex; gap:16px; align-items:center; margin: 8px 0 12px; }
        .info .badge { background: #111827; border:1px solid #374151; border-radius:6px; padding:4px 8px; font-size: 12px; }
        .canvas-wrap { display:flex; justify-content:center; align-items:center; width:100%; overflow:auto; background: linear-gradient(180deg, rgba(255,255,255,0.03), transparent 60%); border-radius: 10px; padding: 8px; }
        canvas { background: var(--floor); border-radius: 8px; border: 1px solid #374151; image-rendering: pixelated; }
        .help { margin-top: 10px; color: var(--muted); font-size: 12px; line-height: 1.6; }
        .level-select { margin-left: auto; }
        select { background: #111827; color: var(--text); border:1px solid #374151; border-radius:8px; padding:6px 8px; }
      </style>
    </head>
    <body>
      <div class=\"wrap\">
        <div class=\"card\">
          <div class=\"title\">
            <h1>推箱子 Sokoban</h1>
            <div class=\"muted\">方向键/WASD 移动 · R 重开 · U 撤销</div>
          </div>
          <div class=\"toolbar\">
            <button id=\"btnPrev\">上一关</button>
            <button id=\"btnReset\">重开本关 (R)</button>
            <button id=\"btnNext\">下一关</button>
            <div class=\"level-select\">
              <select id=\"levelSel\"></select>
            </div>
          </div>
          <div class=\"info\">
            <div class=\"badge\">关卡：<span id=\"levelName\">-</span></div>
            <div class=\"badge\">步数：<span id=\"moves\">0</span></div>
            <div class=\"badge\">箱子：<span id=\"boxes\">0</span>/<span id=\"targets\">0</span></div>
            <div class=\"badge\" id=\"status\"></div>
          </div>
          <div class=\"canvas-wrap\">
            <canvas id=\"game\" width=\"480\" height=\"480\" aria-label=\"推箱子游戏画布\"></canvas>
          </div>
          <div class=\"help\">
            规则：推动箱子到所有目标点（黄色）即可过关。玩家不能穿墙，也不能拉箱子，只能推动。<br/>
            操作：方向键或 WASD 移动；R 重新开始；U 撤销一步；也可以使用按钮切换关卡。
          </div>
        </div>
      </div>

      <script>
      // 关卡定义（使用传统 Sokoban 字符）
      // # 墙,   ' ' 地板,   . 目标,   @ 玩家,   $ 箱子,   * 箱子在目标,   + 玩家在目标
      const LEVELS = [
        {
          name: '入门-1',
          map: [
            '#####',
            '#@$.#',
            '#####'
          ]
        },
        {
          name: '入门-2',
          map: [
            '######',
            '#   .#',
            '# $$ #',
            '# @  #',
            '######'
          ]
        },
        {
          name: '小试牛刀',
          map: [
            '########',
            '#  .   #',
            '#  $   #',
            '# ###  #',
            '#   $  #',
            '#  .  @#',
            '########'
          ]
        }
      ];

      // 渲染参数
      const TILE = 40; // 单元格像素尺寸
      const WALL_COLOR = getCSS('--wall');
      const FLOOR_COLOR = getCSS('--floor');
      const TARGET_COLOR = getCSS('--target');
      const BOX_COLOR = getCSS('--box');
      const BOX_OK_COLOR = getCSS('--box-ok');
      const PLAYER_COLOR = getCSS('--player');

      function getCSS(name){
        return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
      }

      // 游戏状态
      let levelIndex = 0;
      let base = [];   // 基底：'#'墙，' '地，'.'目标
      let boxes = [];  // 2D boolean
      let targets = []; // 目标坐标数组 [{x,y}]
      let player = {x:0, y:0};
      let moves = 0;
      let history = []; // 用于撤销：存储动作记录

      const canvas = document.getElementById('game');
      const ctx = canvas.getContext('2d');
      const levelNameEl = document.getElementById('levelName');
      const movesEl = document.getElementById('moves');
      const boxesEl = document.getElementById('boxes');
      const targetsEl = document.getElementById('targets');
      const statusEl = document.getElementById('status');
      const selEl = document.getElementById('levelSel');

      // 初始化下拉
      LEVELS.forEach((lv, idx) => {
        const opt = document.createElement('option');
        opt.value = idx; opt.textContent = `${idx+1}. ${lv.name}`;
        selEl.appendChild(opt);
      });
      selEl.addEventListener('change', (e)=>{
        loadLevel(parseInt(e.target.value,10));
      });

      document.getElementById('btnPrev').addEventListener('click', ()=>{
        if(levelIndex > 0) loadLevel(levelIndex-1);
      });
      document.getElementById('btnNext').addEventListener('click', ()=>{
        if(levelIndex < LEVELS.length-1) loadLevel(levelIndex+1);
      });
      document.getElementById('btnReset').addEventListener('click', ()=>{
        loadLevel(levelIndex);
      });

      // 载入关卡
      function loadLevel(idx){
        levelIndex = idx;
        const lv = LEVELS[idx];
        levelNameEl.textContent = lv.name;
        selEl.value = idx;

        const h = lv.map.length;
        const w = Math.max(...lv.map.map(r => r.length));
        // 调整画布尺寸
        canvas.width = w * TILE;
        canvas.height = h * TILE;

        base = Array.from({length: h}, () => Array(w).fill(' '));
        boxes = Array.from({length: h}, () => Array(w).fill(false));
        targets = [];
        player = {x:0, y:0};
        moves = 0; history = [];

        for(let y=0; y<h; y++){
          const row = lv.map[y];
          for(let x=0; x<w; x++){
            const c = row[x] || ' ';
            if(c === '#') base[y][x] = '#';
            else if(c === '.' || c === '+' || c === '*') {
              base[y][x] = '.';
              targets.push({x,y});
            } else {
              base[y][x] = ' ';
            }

            if(c === '@' || c === '+') { player = {x,y}; }
            if(c === '$' || c === '*') { boxes[y][x] = true; }
          }
        }
        boxesEl.textContent = countBoxesOnTargets();
        targetsEl.textContent = targets.length;
        movesEl.textContent = moves;
        statusEl.textContent = '';
        draw();
      }

      function countBoxesOnTargets(){
        let c = 0;
        for(const t of targets){ if(boxes[t.y][t.x]) c++; }
        return c;
      }

      function draw(){
        const h = base.length; const w = base[0].length;
        ctx.clearRect(0,0,canvas.width, canvas.height);

        // 背板与目标
        for(let y=0; y<h; y++){
          for(let x=0; x<w; x++){
            const px = x*TILE, py = y*TILE;
            // 地板
            ctx.fillStyle = FLOOR_COLOR;
            ctx.fillRect(px, py, TILE, TILE);
            // 墙
            if(base[y][x] === '#'){
              ctx.fillStyle = WALL_COLOR;
              ctx.fillRect(px, py, TILE, TILE);
              // 做一点阴影
              ctx.fillStyle = 'rgba(255,255,255,0.04)';
              ctx.fillRect(px, py, TILE, 6);
              ctx.fillStyle = 'rgba(0,0,0,0.2)';
              ctx.fillRect(px, py+TILE-6, TILE, 6);
              continue;
            }
            // 目标点
            if(base[y][x] === '.'){
              ctx.fillStyle = TARGET_COLOR;
              const r = Math.floor(TILE*0.2);
              ctx.beginPath();
              ctx.arc(px+TILE/2, py+TILE/2, r, 0, Math.PI*2);
              ctx.fill();
            }
          }
        }

        // 箱子
        for(let y=0; y<base.length; y++){
          for(let x=0; x<base[0].length; x++){
            if(boxes[y][x]){
              const px = x*TILE, py = y*TILE;
              const onTarget = (base[y][x] === '.');
              ctx.fillStyle = onTarget ? BOX_OK_COLOR : BOX_COLOR;
              const m = 6;
              ctx.fillRect(px+m, py+m, TILE-2*m, TILE-2*m);
              // 边框与高光
              ctx.strokeStyle = 'rgba(0,0,0,0.35)';
              ctx.lineWidth = 2;
              ctx.strokeRect(px+m+1, py+m+1, TILE-2*m-2, TILE-2*m-2);
              ctx.fillStyle = 'rgba(255,255,255,0.06)';
              ctx.fillRect(px+m+2, py+m+2, TILE-2*m-4, 8);
            }
          }
        }

        // 玩家
        const px = player.x*TILE, py = player.y*TILE;
        ctx.fillStyle = PLAYER_COLOR;
        ctx.beginPath();
        ctx.arc(px+TILE/2, py+TILE/2, Math.floor(TILE*0.35), 0, Math.PI*2);
        ctx.fill();
        ctx.fillStyle = 'rgba(255,255,255,0.12)';
        ctx.beginPath();
        ctx.arc(px+TILE/2-6, py+TILE/2-6, Math.floor(TILE*0.12), 0, Math.PI*2);
        ctx.fill();
      }

      function isWall(x,y){ return base[y] && base[y][x] === '#'; }
      function hasBox(x,y){ return boxes[y] && boxes[y][x]; }

      function move(dx, dy){
        const nx = player.x + dx;
        const ny = player.y + dy;
        if(!base[ny] || base[ny][nx] === undefined) return; // 越界
        if(isWall(nx, ny)) return; // 墙

        // 目标格上有箱子？尝试推动
        if(hasBox(nx, ny)){
          const bx = nx + dx; const by = ny + dy;
          if(!base[by] || base[by][bx] === undefined) return; // 越界
          if(isWall(bx, by) || hasBox(bx, by)) return; // 被堵住
          // 记录历史（用于撤销）：包含玩家原坐标、被推动箱子的目的地
          history.push({
            type: 'push',
            px: player.x, py: player.y,
            from: {x: nx, y: ny}, to: {x: bx, y: by}
          });
          boxes[ny][nx] = false;
          boxes[by][bx] = true;
          player.x = nx; player.y = ny;
        } else {
          // 普通移动
          history.push({ type: 'move', px: player.x, py: player.y });
          player.x = nx; player.y = ny;
        }
        moves++;
        movesEl.textContent = moves;
        boxesEl.textContent = countBoxesOnTargets();
        if(checkWin()){
          statusEl.textContent = '恭喜过关！';
          // 自动进入下一关（如果有）
          if(levelIndex < LEVELS.length-1){
            setTimeout(() => loadLevel(levelIndex+1), 600);
          }
        } else {
          statusEl.textContent = '';
        }
        draw();
      }

      function undo(){
        const last = history.pop();
        if(!last) return;
        if(last.type === 'move'){
          player.x = last.px; player.y = last.py;
          moves++;
        } else if(last.type === 'push'){
          // 把箱子退回
          boxes[last.to.y][last.to.x] = false;
          boxes[last.from.y][last.from.x] = true;
          player.x = last.px; player.y = last.py;
          moves++;
        }
        movesEl.textContent = moves;
        boxesEl.textContent = countBoxesOnTargets();
        statusEl.textContent = '';
        draw();
      }

      function checkWin(){
        // 所有目标都有箱子
        for(const t of targets){ if(!boxes[t.y][t.x]) return false; }
        return targets.length > 0; // 至少有目标
      }

      // 键盘事件
      window.addEventListener('keydown', (e)=>{
        const k = e.key.toLowerCase();
        if(['arrowup','w'].includes(k)) { e.preventDefault(); move(0,-1); }
        else if(['arrowdown','s'].includes(k)) { e.preventDefault(); move(0,1); }
        else if(['arrowleft','a'].includes(k)) { e.preventDefault(); move(-1,0); }
        else if(['arrowright','d'].includes(k)) { e.preventDefault(); move(1,0); }
        else if(k === 'r') { e.preventDefault(); loadLevel(levelIndex); }
        else if(k === 'u') { e.preventDefault(); undo(); }
      }, {passive:false});

      // 初始加载
      loadLevel(0);
      </script>
    </body>
    </html>
    """


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
