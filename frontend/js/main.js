// 简单示例，从后端获取游戏列表并展示
async function loadGames() {
    const resp = await fetch('http://127.0.0.1:8000/games/');  // 向后端请求游戏列表
    const games = await resp.json();  // 将响应数据转换为 JSON
    const gameListDiv = document.getElementById('game-list');  // 获取游戏列表显示的 DOM
    gameListDiv.innerHTML = '';  // 清空内容

    games.forEach(g => {
        const div = document.createElement('div');  // 为每个游戏创建一个 <div> 元素
        div.innerHTML = `
            <strong>${g.title}</strong> 
            <button data-id="${g.id}" class="edit-game-btn">编辑</button> 
            <button data-id="${g.id}" class="play-game-btn">游玩</button>
        `;
        gameListDiv.appendChild(div);
    });

    // 修改 "编辑" 按钮逻辑，点击后跳转到 edit_game.html 页面，带上 game_id 参数
    document.querySelectorAll('.edit-game-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const gameId = e.target.getAttribute('data-id');  // 获取游戏ID
            window.location.href = `http://127.0.0.1:8001/edit_game.html?game_id=${gameId}`;
        });
    });
    document.querySelectorAll('.play-game-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const gameId = e.target.getAttribute('data-id');
            // 跳转到 play_game.html
            // 假设你的前端域名为 https://my-frontend.com
            // 那就写:
            // window.location.href = `https://my-frontend.com/play_game.html?game_id=${gameId}`;
            // 本地测试时:
            window.location.href = `http://127.0.0.1:8001/play_game.html?game_id=${gameId}`;
        });
    });
    
    // 游玩按钮功能留待 play_game.js 实现
}

document.getElementById('create-game-btn').addEventListener('click', () => {
    document.getElementById('create-game-form').style.display = 'block';
});

document.getElementById('save-game-btn').addEventListener('click', async () => {
    const title = document.getElementById('game-title').value;  // 获取标题
    const background = document.getElementById('game-background').value;  // 获取背景

    const resp = await fetch('http://127.0.0.1:8000/games/', {  // 发送POST请求创建游戏
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            title,
            background,
            random_entries: []  // 添加默认空数组
        })
    });    
    if(resp.ok) {
        alert('创建成功');
        document.getElementById('create-game-form').style.display = 'none';
        await loadGames();  // 重新加载游戏列表
    } else {
        alert('创建失败');
    }
});

// 初始化页面时加载游戏列表
loadGames();
