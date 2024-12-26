// js/main.js

// 设置全局的 baseURL（后端 API 地址）和 frontBaseURL（前端地址）
const baseURL = 'http://127.0.0.1:8000';  // 后端 API 基础地址
const frontBaseURL = 'http://127.0.0.1:8001';  // 前端页面基础地址

// 从后端获取游戏列表并展示
async function loadGames() {
    try {
        const resp = await fetch(`${baseURL}/games/`);
        if (!resp.ok) {
            throw new Error('无法获取游戏列表');
        }

        const games = await resp.json();
        const gameListDiv = document.getElementById('game-list');
        gameListDiv.innerHTML = ''; // 清空内容

        games.forEach(g => {
            const gameCard = document.createElement('div');
            gameCard.classList.add('game-card');
            gameCard.innerHTML = `
                <strong>${g.title}</strong>
                <button class="btn btn-primary edit-game-btn" data-id="${g.id}">编辑</button>
                <button class="btn btn-success play-game-btn" data-id="${g.id}">游玩</button>
            `;
            gameListDiv.appendChild(gameCard);
        });

        // 添加事件监听器
        document.querySelectorAll('.edit-game-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const gameId = e.target.getAttribute('data-id');
                window.location.href = `${frontBaseURL}/edit_game.html?game_id=${gameId}`;
            });
        });
        document.querySelectorAll('.play-game-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const gameId = e.target.getAttribute('data-id');
                window.location.href = `${frontBaseURL}/play_game.html?game_id=${gameId}`;
            });
        });
    } catch (error) {
        console.error(error.message);
    }
}


// 显示创建游戏表单
document.getElementById('create-game-btn').addEventListener('click', () => {
    document.getElementById('create-game-form').style.display = 'block';
});

// 保存新游戏并刷新游戏列表
document.getElementById('save-game-btn').addEventListener('click', async () => {
    const title = document.getElementById('game-title').value.trim();  // 获取标题
    const background = document.getElementById('game-background').value.trim();  // 获取背景

    if (!title || !background) {
        alert('请填写所有字段');
        return;
    }

    try {
        const resp = await fetch(`${baseURL}/games/`, {  // 使用 baseURL 发送POST请求
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
            document.getElementById('game-title').value = '';
            document.getElementById('game-background').value = '';
            await loadGames();  // 重新加载游戏列表
        } else {
            const errorData = await resp.json();
            alert(`创建失败: ${errorData.message || '未知错误'}`);
        }
    } catch (error) {
        alert(`创建失败: ${error.message}`);
    }
});

// 初始化页面时加载游戏列表
window.addEventListener('DOMContentLoaded', loadGames);
