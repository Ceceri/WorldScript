const baseURL = "http://127.0.0.1:8000";  // 后端 API 地址
let currentAttributes = {};  // 当前玩家属性
let occurredEvents = []; // 记录已发生事件的ID

// 初始化游戏
async function initGame() {
    const gameId = new URLSearchParams(window.location.search).get('game_id');
    if (!gameId) {
        alert("请提供游戏ID！");
        return;
    }

    // 获取游戏信息
    const gameInfoResp = await fetch(`${baseURL}/games/${gameId}`);
    const gameInfo = await gameInfoResp.json();
    document.getElementById('game-title').innerText = gameInfo.title;
    document.getElementById('game-background').innerText = gameInfo.background;

    // 加载初始玩家属性
    const attributesResp = await fetch(`${baseURL}/attributes?game_id=${gameId}`);
    const attributes = await attributesResp.json();
    attributes.forEach(attr => {
        currentAttributes[attr.name] = attr.initial_value;
    });

    updateAttributesDisplay();
    document.getElementById('start-game-btn').addEventListener('click', () => startGame(gameId));
}

// 更新玩家属性显示
function updateAttributesDisplay() {
    const attributeList = document.getElementById('attribute-list');
    attributeList.innerHTML = '';
    for (const [name, value] of Object.entries(currentAttributes)) {
        const li = document.createElement('li');
        li.innerText = `${name}: ${value}`;
        attributeList.appendChild(li);
    }
}

// 显示事件和选项
function displayEvent(event) {
    document.getElementById('event-title').innerText = event.title;
    document.getElementById('event-description').innerText = event.description;

    const optionsDiv = document.getElementById('options');
    optionsDiv.innerHTML = '';
    event.options.forEach(option => {
        const button = document.createElement('button');
        button.innerText = option.text;
        button.addEventListener('click', () => selectOption(event, option));
        optionsDiv.appendChild(button);
    });

    document.getElementById('event-section').style.display = 'block';
}

// 检查结局条件
async function checkEndings(gameId) {
    const resp = await fetch(`${baseURL}/endings?game_id=${gameId}`);
    const endings = await resp.json();

    for (const ending of endings) {
        if (checkConditions(currentAttributes, ending.trigger_conditions)) {
            alert(ending.description || "游戏结束！");
            return true;
        }
    }
    return false;
}

// 检查多个条件是否满足
function checkConditions(attributes, conditions) {
    return conditions.every(condition => {
        const attrValue = attributes[condition.attribute] || 0;
        const operator = condition.operator;
        const value = condition.value;

        return evaluateCondition(attrValue, operator, value);
    });
}

// 评估单个条件
function evaluateCondition(attrValue, operator, value) {
    switch (operator) {
        case ">": return attrValue > value;
        case ">=": return attrValue >= value;
        case "<": return attrValue < value;
        case "<=": return attrValue <= value;
        case "==": return attrValue === value;
        default: return false;
    }
}

// 开始游戏，加载符合条件的事件
async function startGame(gameId) {
    if (await checkEndings(gameId)) {
        return;
    }

    const payload = {
        player_attributes: currentAttributes,
        occurred_events: occurredEvents // 将发生过的事件ID传递给后端
    };

    const resp = await fetch(`${baseURL}/events/random?game_id=${gameId}`, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    if (!resp.ok) {
        console.error("Failed to fetch event:", resp.status);
        alert("加载事件失败！");
        return;
    }

    const event = await resp.json();
    if (event) {
        displayEvent(event);

        // 将当前事件的ID添加到已发生事件列表中
        occurredEvents.push(event.id);
    } else {
        alert("没有符合条件的事件，游戏结束！");
    }
}

// 选择选项并应用影响
async function selectOption(event, option) {
    const changes = option.result_attribute_changes;

    // 确保 result_attribute_changes 是一个数组
    if (!Array.isArray(changes)) {
        console.error("Invalid result_attribute_changes:", changes);
        alert("选项的属性变化数据无效！");
        return;
    }

    // 如果没有属性变化，直接返回
    if (changes.length === 0) {
        console.warn("No attribute changes to apply.");
        alert("没有属性变化可应用！");
        return;
    }

    // 遍历每个属性变化并应用
    changes.forEach(change => {
        if (!change || typeof change !== 'object') {
            console.warn("Invalid change object:", change);
            return;
        }

        const { attribute, value, operation } = change;

        // 验证字段完整性
        if (!attribute || value === undefined || !operation) {
            console.warn(`无效的属性变化定义: 属性=${attribute}, 数据=`, change);
            return;
        }

        // 应用属性变化
        const oldValue = currentAttributes[attribute] || 0;
        const newValue = applyOperation(oldValue, { value, operation });
        console.log(`Attribute changed: ${attribute}, Old Value: ${oldValue}, New Value: ${newValue}`);
        currentAttributes[attribute] = newValue;
    });

    updateAttributesDisplay();

    alert(option.impact_description || "你选择了该选项。");

    // 检查是否触发结局
    if (await checkEndings(event.game_id)) {
        return;
    }

    // 继续游戏
    startGame(event.game_id);
}

// 属性变化逻辑
function applyOperation(currentValue, change) {
    const operation = change.operation || "add";
    const value = change.value;

    switch (operation) {
        case "add": return currentValue + value;
        case "subtract": return currentValue - value;
        case "multiply": return currentValue * value;
        case "divide": return value !== 0 ? currentValue / value : currentValue;
        default: return currentValue;
    }
}

// 初始化游戏页面
initGame();
