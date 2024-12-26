// ========== 全局常量/变量 & DOM 选择 ==========
const urlParams = new URLSearchParams(window.location.search);
const gameId = urlParams.get('game_id');
const baseURL = "http://127.0.0.1:8000";  // 后端服务地址，请根据实际情况修改

if (!gameId) {
    alert("请在URL中指定game_id参数，如 ?game_id=1");
}

// -- 游戏信息管理 --
const gameTitleInput = document.getElementById('game-title');
const gameBackgroundInput = document.getElementById('game-background');
const updateGameBtn = document.getElementById('update-game-btn');

// -- 属性管理 --
const attributeListDiv = document.getElementById('attribute-list');
const addAttrBtn = document.getElementById('add-attr-btn');
const newAttrNameInput = document.getElementById('new-attr-name');
const newAttrValueInput = document.getElementById('new-attr-value');

// -- 事件管理 (列表+表单) --
const eventListDiv = document.getElementById('event-list');
const saveEventBtn = document.getElementById('save-event-btn');
const newEventIdInput = document.getElementById('new-event-id');
const newEventTitleInput = document.getElementById('new-event-title');
const newEventDescInput = document.getElementById('new-event-desc');

// -- 选项管理 --
const optionSection = document.getElementById('option-section');
const optionListDiv = document.getElementById('option-list');
const currentEventIdSpan = document.getElementById('current-event-id');
const addBlankOptionBtn = document.getElementById('add-blank-option-btn');

// -- 使用 LLM 生成事件内容 --
const llmGenerateBtn = document.getElementById('llm-generate-btn');

// -- 事件范围条件 --
const rangeAttributeSelect = document.getElementById('range-attribute');
const rangeMinInput = document.getElementById('range-min');
const rangeMaxInput = document.getElementById('range-max');

// -- 结局管理 (列表+表单) --
const endingListDiv = document.getElementById('ending-list');

// 这里是「多条件结局」相关的 DOM
let newEndingConditions = [];  // 存储当前要添加的结局的多条条件
const newEndingDescInput = document.getElementById('new-ending-desc');
const endingConditionListDiv = document.getElementById('ending-condition-list');
const endingConditionTypeSelect = document.getElementById('ending-condition-type');
const addEndingConditionBtn = document.getElementById('add-ending-condition-btn');
const addEndingBtn = document.getElementById('add-ending-btn');

// -- 结局属性下拉框 (仅在"属性比较"类型时用) --
const endingAttributeSelect = document.getElementById('ending-attribute-select');

// 全局对象，用于在前端暂存当前正在编辑的事件数据
let currentEventData = {
    id: null,
    title: "",
    description: "",
    range_condition: null,
    options: []
};

// 全局属性列表（用于下拉菜单）
let globalAttributes = [];

// ========== 初始化：加载数据 ==========
(async function init() {
    await loadGameInfo();
    await loadAttributes();
    await loadEndingAttributes();
    await loadEventAttributes();
    await loadEvents();
    await loadEndings();
})();

// ========== 游戏信息 ==========
async function loadGameInfo() {
    try {
        const resp = await fetch(`${baseURL}/games/${gameId}`);
        if (!resp.ok) {
            throw new Error("加载游戏信息失败");
        }
        const game = await resp.json();
        gameTitleInput.value = game.title;
        gameBackgroundInput.value = game.background || "";
    } catch (error) {
        console.error(error);
        alert(error.message);
    }
}

updateGameBtn.addEventListener('click', async () => {
    const title = gameTitleInput.value.trim() || null;
    const background = gameBackgroundInput.value.trim() || null;
    const random_entries = [];

    const payload = { title, background, random_entries };

    try {
        const resp = await fetch(`${baseURL}/games/${gameId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (resp.ok) {
            alert("更新成功");
        } else {
            const error = await resp.json();
            throw new Error(error.detail || "未知错误");
        }
    } catch (error) {
        console.error("更新失败:", error);
        alert(`更新失败: ${error.message}`);
    }
});

// ========== 属性管理 ==========
async function loadAttributes() {
    try {
        const resp = await fetch(`${baseURL}/attributes?game_id=${gameId}`);
        if (!resp.ok) {
            throw new Error("加载属性失败");
        }
        const attrs = await resp.json();
        globalAttributes = attrs; // 存储到全局变量中
        attributeListDiv.innerHTML = "";

        attrs.forEach(a => {
            const div = document.createElement('div');
            div.innerHTML = `
                <strong>${a.name}</strong> (初始值: ${a.initial_value})
                <button data-id="${a.id}" class="del-attr-btn">删除</button>
                <button data-id="${a.id}" class="edit-attr-btn">编辑</button>
            `;
            attributeListDiv.appendChild(div);
        });

        // 绑定属性删除事件
        document.querySelectorAll('.del-attr-btn').forEach(btn => {
            btn.addEventListener('click', async () => {
                const id = btn.getAttribute('data-id');
                try {
                    const r = await fetch(`${baseURL}/attributes/${id}`, { method: 'DELETE' });
                    if (r.ok) {
                        await loadAttributes();
                        await loadEndingAttributes();
                        await loadEventAttributes();
                    } else {
                        throw new Error("删除失败");
                    }
                } catch (error) {
                    console.error(error);
                    alert(error.message);
                }
            });
        });

        // 绑定属性编辑事件
        document.querySelectorAll('.edit-attr-btn').forEach(btn => {
            btn.addEventListener('click', async () => {
                const id = btn.getAttribute('data-id');
                const newVal = prompt("输入新的初始值:", "");
                if (newVal !== null && newVal.trim() !== "") {
                    const payload = { initial_value: parseFloat(newVal) };
                    try {
                        const resp = await fetch(`${baseURL}/attributes/${id}`, {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(payload)
                        });
                        if (resp.ok) {
                            await loadAttributes();
                            await loadEndingAttributes();
                            await loadEventAttributes();
                        } else {
                            const error = await resp.json();
                            throw new Error(error.detail || "更新失败");
                        }
                    } catch (error) {
                        console.error("Error response:", error);
                        alert(`更新失败: ${error.message}`);
                    }
                }
            });
        });

        updateSelects(attrs);
    } catch (error) {
        console.error(error);
        attributeListDiv.innerHTML = error.message;
        alert(error.message);
    }
}

function updateSelects(attrs) {
    // 用于事件范围条件
    rangeAttributeSelect.innerHTML = "";
    attrs.forEach(attr => {
        const option = document.createElement('option');
        option.value = attr.name;
        option.textContent = attr.name;
        rangeAttributeSelect.appendChild(option);
    });

    // 用于结局里"属性比较"时可选的属性
    endingAttributeSelect.innerHTML = "";
    attrs.forEach(attr => {
        const option = document.createElement('option');
        option.value = attr.name;
        option.textContent = attr.name;
        endingAttributeSelect.appendChild(option);
    });
}

// 添加属性
addAttrBtn.addEventListener('click', async () => {
    const name = newAttrNameInput.value.trim();
    const val = parseFloat(newAttrValueInput.value);
    if (!name) {
        alert("属性名称不能为空");
        return;
    }
    try {
        const resp = await fetch(`${baseURL}/attributes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ game_id: parseInt(gameId), name, initial_value: val })
        });
        if (resp.ok) {
            newAttrNameInput.value = "";
            newAttrValueInput.value = "";
            await loadAttributes();
            await loadEndingAttributes();
            await loadEventAttributes();
        } else {
            const error = await resp.json();
            throw new Error(error.detail || "添加属性失败");
        }
    } catch (error) {
        console.error("添加属性失败:", error);
        alert(error.message);
    }
});

// ========== 事件列表、事件编辑 + 选项管理 ==========
async function loadEvents() {
    try {
        const resp = await fetch(`${baseURL}/events?game_id=${gameId}`);
        if (!resp.ok) {
            throw new Error("加载事件失败");
        }
        const events = await resp.json();
        eventListDiv.innerHTML = "";
        events.forEach(e => {
            const div = document.createElement('div');
            div.innerHTML = `
                <strong>ID:${sanitize(e.id)}</strong> - ${sanitize(e.title)}
                <button data-id="${e.id}" class="del-event-btn">删除</button>
                <button data-id="${e.id}" class="edit-event-btn">编辑</button>
                <button data-id="${e.id}" class="options-event-btn">管理选项</button>
            `;
            eventListDiv.appendChild(div);
        });

        // 删除事件
        document.querySelectorAll('.del-event-btn').forEach(btn => {
            btn.addEventListener('click', async () => {
                const id = btn.getAttribute('data-id');
                if (confirm("确定要删除这个事件吗？")) {
                    try {
                        const resp = await fetch(`${baseURL}/events/${id}`, { method: 'DELETE' });
                        if (resp.ok) {
                            loadEvents();
                        } else {
                            throw new Error("删除事件失败");
                        }
                    } catch (error) {
                        console.error(error);
                        alert(error.message);
                    }
                }
            });
        });

        // 编辑事件标题
        document.querySelectorAll('.edit-event-btn').forEach(btn => {
            btn.addEventListener('click', async () => {
                const id = btn.getAttribute('data-id');
                const newTitle = prompt("输入新的事件标题:");
                if (newTitle !== null && newTitle.trim() !== "") {
                    const payload = {
                        title: newTitle.trim(),
                        description: null,
                        range_condition: null
                    };
                    try {
                        const resp = await fetch(`${baseURL}/events/${id}`, {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(payload)
                        });
                        if (resp.ok) {
                            alert("事件标题更新成功");
                            loadEvents();
                        } else {
                            const error = await resp.json();
                            throw new Error(error.detail || "更新失败");
                        }
                    } catch (error) {
                        console.error("更新失败:", error);
                        alert(`更新失败: ${error.message}`);
                    }
                }
            });
        });

        // 管理选项
        document.querySelectorAll('.options-event-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const eventId = btn.getAttribute('data-id');
                showOptionsForEvent(eventId);
            });
        });
    } catch (error) {
        console.error(error);
        eventListDiv.innerHTML = error.message;
        alert(error.message);
    }
}

async function showOptionsForEvent(eventId) {
    currentEventData = {
        id: eventId,
        title: "",
        description: "",
        range_condition: null,
        options: []
    };

    try {
        // 获取事件详情
        const respEvent = await fetch(`${baseURL}/events/${eventId}`);
        if (!respEvent.ok) {
            throw new Error("加载事件详情失败");
        }
        const eventData = await respEvent.json();
        currentEventData.title = eventData.title || "";
        currentEventData.description = eventData.description || "";
        currentEventData.range_condition = eventData.range_condition || null;

        // 获取选项数据
        const respOptions = await fetch(`${baseURL}/options?event_id=${eventId}`);
        if (!respOptions.ok) {
            throw new Error("加载选项失败");
        }
        const options = await respOptions.json();
        currentEventData.options = options.map(o => ({
            id: o.id,
            text: o.text,
            impact_description: o.impact_description,
            // 确保 result_attribute_changes 是数组
            result_attribute_changes: Array.isArray(o.result_attribute_changes)
                ? o.result_attribute_changes
                : (o.result_attribute_changes ? [o.result_attribute_changes] : []),
            triggers_ending: o.triggers_ending,
            ending_description: o.ending_description || null
        }));

        // 将数据填入表单
        newEventIdInput.value = currentEventData.id;
        newEventTitleInput.value = currentEventData.title;
        newEventDescInput.value = currentEventData.description || "";
        currentEventIdSpan.textContent = currentEventData.id;

        optionSection.style.display = 'block';
        renderOptionInputs();
    } catch (error) {
        console.error(error);
        alert(error.message);
    }
}

// 使用 LLM 生成事件描述和选项
llmGenerateBtn.addEventListener('click', async () => {
    const title = newEventTitleInput.value.trim();
    const description = newEventDescInput.value.trim();
    const background = gameBackgroundInput.value.trim();

    if (!title || !description || !background) {
        alert("标题、描述和背景不能为空！");
        return;
    }

    // 禁用按钮并显示加载动画
    llmGenerateBtn.disabled = true;
    llmGenerateBtn.textContent = "加载中...";

    try {
        // 获取游戏属性
        const attrResp = await fetch(`${baseURL}/attributes?game_id=${gameId}`);
        if (!attrResp.ok) {
            throw new Error("加载属性失败");
        }
        const attributes = await attrResp.json();

        const response = await fetch(`${baseURL}/events/llm_generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, description, background, attributes })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "生成失败！");
        }

        const data = await response.json();
        // 检查 data.options
        if (!Array.isArray(data.options)) {
            console.warn("LLM 返回的 options 不是数组，尝试将其转换为数组。", data.options);
            data.options = Array.isArray(data.options) ? data.options : [data.options];
        }

        // 将LLM生成的描述与选项存入currentEventData
        currentEventData.id = newEventIdInput.value.trim();
        currentEventData.title = newEventTitleInput.value.trim();
        currentEventData.description = data.extended_description;

        currentEventData.options = data.options.map(opt => ({
            text: opt.text,
            impact_description: opt.impact_description || "",
            result_attribute_changes: opt.result_attribute_changes || [],
            triggers_ending: opt.triggers_ending || false,
            ending_description: opt.ending_description || null
        }));

        newEventDescInput.value = data.extended_description;
        currentEventIdSpan.textContent = currentEventData.id || "";
        optionSection.style.display = 'block';

        renderOptionInputs();
        alert("生成成功！请检查和编辑选项。");
    } catch (error) {
        console.error("Error generating content:", error);
        alert(`生成失败：${error.message}`);
    } finally {
        // 重新启用按钮并恢复文本
        llmGenerateBtn.disabled = false;
        llmGenerateBtn.textContent = "使用 LLM 生成扩写和选项";
    }
});

// 渲染选项输入框
function renderOptionInputs() {
    optionListDiv.innerHTML = '';

    // 确保每个选项的 result_attribute_changes 为数组
    currentEventData.options.forEach((option, index) => {
        if (!option.result_attribute_changes) {
            console.warn(`选项 ${index + 1} 的 result_attribute_changes 未定义或为假值，自动初始化为空数组。`);
            option.result_attribute_changes = [];
        } else if (!Array.isArray(option.result_attribute_changes)) {
            console.warn(`选项 ${index + 1} 的 result_attribute_changes 不是数组，当前值:`, option.result_attribute_changes);
            // 将字典转换为数组格式
            option.result_attribute_changes = Object.entries(option.result_attribute_changes).map(([key, value]) => ({
                attribute: key,
                operation: value.operation,
                value: value.value
            }));
        }
    });

    // 如果没有选项，添加一个空白选项
    if (currentEventData.options.length === 0) {
        currentEventData.options.push({
            text: "",
            impact_description: "",
            result_attribute_changes: [],
            triggers_ending: false,
            ending_description: null
        });
    }

    currentEventData.options.forEach((option, index) => {
        const div = document.createElement('div');
        div.className = 'option-input';
        div.innerHTML = `
            <hr>
            <label>选项 ${index + 1}:</label><br>
            <label>描述:</label> <input type="text" class="option-text" value="${sanitize(option.text)}" /><br>
            <label>影响描述:</label> <input type="text" class="impact-description" value="${sanitize(option.impact_description)}" /><br>
            <label>触发结局:</label> <input type="checkbox" class="option-ending-check" ${option.triggers_ending ? 'checked' : ''}><br>
            <label>结局描述(可选):</label> <input type="text" class="option-ending-desc" value="${sanitize(option.ending_description)}" /><br>
            
            <h4>属性变化</h4>
            <div class="attribute-changes-list"></div>
            <div class="attribute-change-add">
                <select class="attr-select"></select>
                <select class="operation-select">
                    <option value="add">加法(+)</option>
                    <option value="subtract">减法(-)</option>
                    <option value="multiply">乘法(×)</option>
                    <option value="divide">除法(÷)</option>
                </select>
                <input type="number" class="attr-value-input" placeholder="数值">
                <button class="add-attr-change-btn">添加属性变化</button>
            </div>

            <button class="remove-option-btn">删除此选项</button>
        `;

        // 属性下拉菜单
        const attrSelect = div.querySelector('.attr-select');
        globalAttributes.forEach(attr => {
            const opt = document.createElement('option');
            opt.value = attr.name;
            opt.textContent = attr.name;
            attrSelect.appendChild(opt);
        });

        const textInput = div.querySelector('.option-text');
        const impactInput = div.querySelector('.impact-description');
        const endingCheck = div.querySelector('.option-ending-check');
        const endingDescInput = div.querySelector('.option-ending-desc');
        const removeBtn = div.querySelector('.remove-option-btn');

        const attrChangesListDiv = div.querySelector('.attribute-changes-list');
        const addAttrChangeBtn = div.querySelector('.add-attr-change-btn');
        const operationSelect = div.querySelector('.operation-select');
        const attrValueInput = div.querySelector('.attr-value-input');

        // 渲染属性变化
        function renderAttrChanges() {
            attrChangesListDiv.innerHTML = '';
            option.result_attribute_changes.forEach((change, cIndex) => {
                const cDiv = document.createElement('div');
                cDiv.innerHTML = `
                    <select class="attr-select">
                        ${globalAttributes.map(attr => `<option value="${attr.name}" ${attr.name === change.attribute ? 'selected' : ''}>${attr.name}</option>`).join('')}
                    </select>
                    <select class="operation-select">
                        <option value="add" ${change.operation === 'add' ? 'selected' : ''}>加法(+)</option>
                        <option value="subtract" ${change.operation === 'subtract' ? 'selected' : ''}>减法(-)</option>
                        <option value="multiply" ${change.operation === 'multiply' ? 'selected' : ''}>乘法(×)</option>
                        <option value="divide" ${change.operation === 'divide' ? 'selected' : ''}>除法(÷)</option>
                    </select>
                    <input type="number" class="attr-value-input" value="${change.value}" placeholder="数值">
                    <button class="del-attr-change-btn">删除</button>
                `;
                cDiv.querySelector('.del-attr-change-btn').addEventListener('click', () => {
                    option.result_attribute_changes.splice(cIndex, 1);
                    renderAttrChanges();
                });
                attrChangesListDiv.appendChild(cDiv);
            });
        }

        renderAttrChanges(); // 首次渲染

        // 输入变化监听器
        textInput.addEventListener('input', (e) => {
            currentEventData.options[index].text = e.target.value;
        });
        impactInput.addEventListener('input', (e) => {
            currentEventData.options[index].impact_description = e.target.value;
        });
        endingCheck.addEventListener('change', (e) => {
            currentEventData.options[index].triggers_ending = e.target.checked;
        });
        endingDescInput.addEventListener('input', (e) => {
            currentEventData.options[index].ending_description = e.target.value;
        });

        // 添加属性变化按钮
        addAttrChangeBtn.addEventListener('click', () => {
            const selectedAttribute = attrSelect.value;
            const selectedOperation = operationSelect.value;
            const inputValue = parseFloat(attrValueInput.value);
            if (!selectedAttribute) {
                alert("请选择属性！");
                return;
            }
            if (isNaN(inputValue)) {
                alert("请输入有效的数值！");
                return;
            }
            currentEventData.options[index].result_attribute_changes.push({
                attribute: selectedAttribute,
                operation: selectedOperation,
                value: inputValue
            });
            attrValueInput.value = "";
            renderAttrChanges();
        });

        // 删除选项
        removeBtn.addEventListener('click', () => {
            currentEventData.options.splice(index, 1);
            renderOptionInputs();
        });

        optionListDiv.appendChild(div);
    });
}

function getOperationSymbol(operation) {
    switch (operation) {
        case 'add':
            return '+';
        case 'subtract':
            return '-';
        case 'multiply':
            return '×';
        case 'divide':
            return '÷';
        default:
            return operation;
    }
}

// 添加空白选项
addBlankOptionBtn.addEventListener('click', () => {
    currentEventData.options.push({
        text: "",
        impact_description: "",
        result_attribute_changes: [],
        triggers_ending: false,
        ending_description: null
    });
    renderOptionInputs();
});

// 保存事件及选项
saveEventBtn.addEventListener('click', async () => {
    // 获取并处理事件基本信息
    currentEventData.id = parseInt(newEventIdInput.value.trim(), 10); // 确保ID为整数
    currentEventData.title = newEventTitleInput.value.trim();
    currentEventData.description = newEventDescInput.value.trim();

    // 处理 range_condition
    const attribute = rangeAttributeSelect.value;
    const minValue = rangeMinInput.value.trim();
    const maxValue = rangeMaxInput.value.trim();

    let rangeCondition = null;
    if (attribute && (minValue !== "" || maxValue !== "")) {
        rangeCondition = {
            attribute: attribute,
            min_value: minValue !== "" ? parseFloat(minValue) : null,
            max_value: maxValue !== "" ? parseFloat(maxValue) : null
        };
    }
    currentEventData.range_condition = rangeCondition;

    // 验证基本字段是否存在
    if (!currentEventData.id || !currentEventData.title || !currentEventData.description) {
        alert("请输入事件ID、标题和描述！");
        return;
    }

    // 验证并处理选项
    currentEventData.options.forEach((option, index) => {
        if (!Array.isArray(option.result_attribute_changes)) {
            console.warn(`选项 ${index + 1} 的 result_attribute_changes 不是数组，初始化为空数组。`, option.result_attribute_changes);
            option.result_attribute_changes = [];
        }
        // 转成标准结构
        option.result_attribute_changes = option.result_attribute_changes.map(change => ({
            attribute: change.attribute || "",
            operation: change.operation || "add",
            value: parseFloat(change.value) || 0
        }));
    });

    // 构造请求 payload
    const payload = {
        id: parseInt(currentEventData.id, 10),
        game_id: parseInt(gameId, 10),
        title: currentEventData.title,
        description: currentEventData.description,
        range_condition: currentEventData.range_condition || null,
        options: currentEventData.options.map(option => ({
            event_id: parseInt(currentEventData.id, 10),
            text: option.text,
            impact_description: option.impact_description,
            result_attribute_changes: option.result_attribute_changes,
            triggers_ending: option.triggers_ending || false,
            ending_description: option.ending_description || null
        }))
    };
    
    try {
        const response = await fetch(`${baseURL}/events`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
    
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "保存事件失败！");
        }
    
        alert("事件保存成功！");
        loadEvents(); // 重新加载事件列表
    
        // 重置当前编辑数据
        currentEventData = {
            id: null,
            title: "",
            description: "",
            range_condition: null,
            options: []
        };
        optionSection.style.display = 'none';
    } catch (error) {
        console.error("Error saving event:", error);
        alert(`保存失败：${error.message}`);
    }
});

// ========== 结局管理：多条件支持 ==========

// 加载结局列表
async function loadEndings() {
    try {
        const resp = await fetch(`${baseURL}/endings?game_id=${gameId}`);
        if (!resp.ok) {
            throw new Error("加载结局失败");
        }
        const endings = await resp.json();
        endingListDiv.innerHTML = "";
        endings.forEach(ending => {
            const div = document.createElement('div');
            div.innerHTML = `
                <strong>ID:${sanitize(ending.id)}</strong> - ${sanitize(ending.description)}
                <button data-id="${ending.id}" class="del-ending-btn">删除</button>
                <button data-id="${ending.id}" class="edit-ending-btn">编辑</button>
            `;
            endingListDiv.appendChild(div);
        });

        // 删除结局
        document.querySelectorAll('.del-ending-btn').forEach(btn => {
            btn.addEventListener('click', async () => {
                const id = btn.getAttribute('data-id');
                if (confirm("确定要删除这个结局吗？")) {
                    try {
                        const resp = await fetch(`${baseURL}/endings/${id}`, { method: 'DELETE' });
                        if (resp.ok) {
                            loadEndings();
                        } else {
                            throw new Error("删除结局失败");
                        }
                    } catch (error) {
                        console.error(error);
                        alert(error.message);
                    }
                }
            });
        });

        // 编辑结局
        document.querySelectorAll('.edit-ending-btn').forEach(btn => {
            btn.addEventListener('click', async () => {
                const id = btn.getAttribute('data-id');
                const newDesc = prompt("输入新的结局描述:", "");
                if (newDesc !== null && newDesc.trim() !== "") {
                    const payload = { description: newDesc.trim() };
                    try {
                        const resp = await fetch(`${baseURL}/endings/${id}`, {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(payload)
                        });
                        if (resp.ok) {
                            loadEndings();
                        } else {
                            const error = await resp.json();
                            throw new Error(error.detail || "更新失败");
                        }
                    } catch (error) {
                        console.error("Error response:", error);
                        alert(`更新失败: ${error.message}`);
                    }
                }
            });
        });
    } catch (error) {
        console.error(error);
        endingListDiv.innerHTML = error.message;
        alert(error.message);
    }
}

// 加载结局属性列表
async function loadEndingAttributes() {
    try {
        const resp = await fetch(`${baseURL}/attributes?game_id=${gameId}`);
        if (!resp.ok) {
            throw new Error("加载结局属性列表失败！");
        }
        const attributes = await resp.json();
        // 这里只是给 "attribute" 类型做一个初始下拉选用
        endingAttributeSelect.innerHTML = "";
        attributes.forEach(attr => {
            const option = document.createElement('option');
            option.value = attr.name;
            option.textContent = attr.name;
            endingAttributeSelect.appendChild(option);
        });
    } catch (error) {
        console.error("Failed to load attributes for endings:", error);
        alert(error.message);
    }
}

// 加载事件属性列表 (事件range用)
async function loadEventAttributes() {
    try {
        const resp = await fetch(`${baseURL}/attributes?game_id=${gameId}`);
        if (!resp.ok) {
            throw new Error("加载事件属性列表失败！");
        }
        const attributes = await resp.json();
        rangeAttributeSelect.innerHTML = "";
        attributes.forEach(attr => {
            const option = document.createElement('option');
            option.value = attr.name;
            option.textContent = attr.name;
            rangeAttributeSelect.appendChild(option);
        });
    } catch (error) {
        console.error("Failed to load attributes for event range:", error);
        alert(error.message);
    }
}

// ========== 【核心】结局添加：多条件管理 ==========

// 点击"添加条件"时，根据下拉框选项来插入不同类型的条件输入行
addEndingConditionBtn.addEventListener('click', () => {
    // 例如 "attribute" / "item" / "flag"
    const condType = endingConditionTypeSelect.value;

    // 每一条件用一个 div
    const condDiv = document.createElement('div');
    condDiv.classList.add('ending-condition-item');

    // 根据类型渲染不同输入元素
    if (condType === 'attribute') {
        condDiv.innerHTML = `
            <span>[属性比较]</span>
            <select class="attr-select"></select>
            <select class="op-select">
                <option value=">">></option>
                <option value=">=">>=</option>
                <option value="<"><</option>
                <option value="<="><=</option>
                <option value="==">==</option>
            </select>
            <input type="number" class="attr-value-input" placeholder="数值">
            <button class="remove-cond-btn">移除</button>
        `;
        // 填充属性下拉
        const sel = condDiv.querySelector('.attr-select');
        globalAttributes.forEach(attr => {
            const opt = document.createElement('option');
            opt.value = attr.name;
            opt.textContent = attr.name;
            sel.appendChild(opt);
        });
    }
    else if (condType === 'item') {
        condDiv.innerHTML = `
            <span>[物品]</span>
            <input type="text" class="item-name-input" placeholder="物品名称">
            <button class="remove-cond-btn">移除</button>
        `;
    }
    else if (condType === 'flag') {
        condDiv.innerHTML = `
            <span>[flag]</span>
            <input type="text" class="flag-name-input" placeholder="flag名称">
            <select class="flag-value-select">
                <option value="true">true</option>
                <option value="false">false</option>
            </select>
            <button class="remove-cond-btn">移除</button>
        `;
    }

    // 绑定"移除"按钮
    const removeBtn = condDiv.querySelector('.remove-cond-btn');
    if (removeBtn) {
        removeBtn.addEventListener('click', () => {
            condDiv.remove();
        });
    }

    // 加入到列表
    endingConditionListDiv.appendChild(condDiv);
});

// 点击"添加结局"时，收集描述和所有条件
addEndingBtn.addEventListener('click', async () => {
    const desc = newEndingDescInput.value.trim();
    if (!desc) {
        alert("结局描述不能为空！");
        return;
    }
    // 收集多条条件
    const condDivs = document.querySelectorAll('.ending-condition-item');
    newEndingConditions = []; // 清空上次的
    condDivs.forEach(div => {
        // 判断是哪种类型
        const attrSelect = div.querySelector('.attr-select');       // 属性下拉
        const itemInput = div.querySelector('.item-name-input');    // 物品名称
        const flagInput = div.querySelector('.flag-name-input');    // flag名称
        if (attrSelect) {
            // 属性比较
            const attribute = attrSelect.value;
            const operator = div.querySelector('.op-select').value;
            const value = parseFloat(div.querySelector('.attr-value-input').value || "0");
            newEndingConditions.push({
                type: "attribute",
                attribute: attribute,
                operator: operator,
                value: value
            });
        }
        else if (itemInput) {
            // 物品判断
            const itemName = itemInput.value.trim();
            newEndingConditions.push({
                type: "item",
                item_name: itemName
            });
        }
        else if (flagInput) {
            // flag判断
            const flagName = flagInput.value.trim();
            const requiredValue = (div.querySelector('.flag-value-select').value === "true");
            newEndingConditions.push({
                type: "flag",
                flag_name: flagName,
                required_value: requiredValue
            });
        }
    });

    // 构造payload
    const payload = {
        game_id: parseInt(gameId, 10),
        description: desc,
        trigger_conditions: newEndingConditions
    };

    try {
        const resp = await fetch(`${baseURL}/endings/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (!resp.ok) {
            const error = await resp.json();
            throw new Error(error.detail || "添加结局失败");
        }
        alert("结局添加成功！");
        // 清空输入
        newEndingDescInput.value = "";
        endingConditionListDiv.innerHTML = "";
        newEndingConditions = [];
        // 刷新列表
        await loadEndings();
    } catch (error) {
        console.error("Error adding ending:", error);
        alert(`添加结局失败: ${error.message}`);
    }
});

// ========== 工具函数：转义HTML特殊字符，防止XSS ==========
function sanitize(str) {
    if (typeof str !== 'string') return '';
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// 确保选项管理部分始终可见，并允许添加新选项
function initializeNewEvent() {
    currentEventData = {
        id: null,
        title: "",
        description: "",
        range_condition: null,
        options: [{
            text: "",
            impact_description: "",
            result_attribute_changes: [],
            triggers_ending: false,
            ending_description: null
        }]
    };

    newEventIdInput.value = "";
    newEventTitleInput.value = "";
    newEventDescInput.value = "";
    currentEventIdSpan.textContent = "新事件";

    optionSection.style.display = 'block';
    renderOptionInputs();
}

// 在页面加载时初始化新事件
window.addEventListener('DOMContentLoaded', (event) => {
    initializeNewEvent();
});
