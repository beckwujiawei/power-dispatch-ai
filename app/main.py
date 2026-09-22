<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Power Dispatch AI</title>
  <style>
    :root {
      --bg: #08111f;
      --bg-elevated: #0d1a2b;
      --panel: rgba(17, 29, 45, 0.92);
      --panel-strong: rgba(21, 36, 58, 0.96);
      --panel-soft: rgba(24, 39, 60, 0.8);
      --primary: #4da3ff;
      --primary-strong: #2c8ef6;
      --secondary: #8ea7ff;
      --success: #35c58a;
      --warning: #f4b740;
      --danger: #f05d6c;
      --info: #5cc8e8;
      --text: #edf4ff;
      --text-soft: #a5bcda;
      --text-muted: #6f88a6;
      --border: rgba(157, 185, 215, 0.14);
      --shadow: 0 12px 40px rgba(0, 0, 0, 0.24);
      --radius-xl: 22px;
      --radius-lg: 16px;
      --radius-md: 12px;
      --radius-sm: 10px;
    }

    * { box-sizing: border-box; }

    html, body {
      margin: 0;
      min-height: 100%;
      font-family: Inter, "Segoe UI", "Microsoft YaHei", sans-serif;
      background: linear-gradient(180deg, #07111d 0%, #0b1727 100%);
      color: var(--text);
    }

    body {
      display: flex;
      flex-direction: column;
      min-height: 100vh;
    }

    button, select, input, textarea {
      font: inherit;
    }

    .topbar {
      height: 72px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px 0 28px;
      background: rgba(10, 17, 29, 0.84);
      border-bottom: 1px solid var(--border);
      backdrop-filter: blur(12px);
      position: sticky;
      top: 0;
      z-index: 10;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      font-weight: 700;
      letter-spacing: 0.2px;
    }

    .brand-badge {
      width: 36px;
      height: 36px;
      display: grid;
      place-items: center;
      border-radius: 12px;
      background: linear-gradient(135deg, rgba(77,163,255,0.22), rgba(138,143,255,0.25));
      border: 1px solid rgba(125, 178, 255, 0.35);
      box-shadow: inset 0 1px 0 rgba(255,255,255,0.14);
      color: var(--primary);
      font-size: 18px;
    }

    .brand-name {
      font-size: 1.05rem;
      font-weight: 700;
    }

    .topbar-right {
      display: flex;
      align-items: center;
      gap: 14px;
      color: var(--text-soft);
      font-size: 0.84rem;
    }

    .status-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      border-radius: 999px;
      background: rgba(53, 197, 138, 0.1);
      color: var(--success);
      border: 1px solid rgba(53, 197, 138, 0.2);
      font-weight: 600;
    }

    .status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--success);
      box-shadow: 0 0 12px rgba(53, 197, 138, 0.9);
    }

    .workspace {
      display: grid;
      grid-template-columns: 220px minmax(0, 1fr) 340px;
      gap: 18px;
      width: min(1600px, calc(100% - 32px));
      margin: 18px auto 26px;
      min-height: calc(100vh - 120px);
    }

    .panel {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: var(--radius-xl);
      box-shadow: var(--shadow);
    }

    .sidebar {
      padding: 18px 14px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .nav-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px 14px;
      border-radius: 12px;
      color: var(--text-soft);
      text-decoration: none;
      font-weight: 600;
      transition: 0.2s ease;
      border: 1px solid transparent;
    }

    .nav-item:hover {
      background: rgba(255,255,255,0.02);
      border-color: var(--border);
    }

    .nav-item.active {
      background: linear-gradient(135deg, rgba(77,163,255,0.14), rgba(133,139,255,0.12));
      border-color: rgba(102, 175, 255, 0.24);
      color: var(--text);
      box-shadow: inset 0 1px 0 rgba(255,255,255,0.06);
    }

    .nav-icon {
      width: 26px;
      height: 26px;
      display: grid;
      place-items: center;
      border-radius: 8px;
      background: rgba(255,255,255,0.03);
      font-size: 0.9rem;
    }

    .main {
      display: flex;
      flex-direction: column;
      gap: 18px;
      min-width: 0;
    }

    .metric-row {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 16px;
    }

    .metric-card {
      padding: 18px 18px 14px;
      background: linear-gradient(180deg, rgba(17, 29, 45, 0.96), rgba(21, 36, 58, 0.9));
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow);
    }

    .metric-label {
      color: var(--text-soft);
      font-size: 0.78rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }

    .metric-value {
      margin-top: 14px;
      font-size: clamp(1.8rem, 2vw, 2.4rem);
      font-weight: 700;
      letter-spacing: -0.04em;
    }

    .metric-foot {
      margin-top: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      color: var(--text-soft);
      font-size: 0.8rem;
    }

    .chip {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 8px;
      border-radius: 999px;
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      border: 1px solid transparent;
    }

    .chip.success {
      color: var(--success);
      background: rgba(53,197,138,0.08);
      border-color: rgba(53,197,138,0.2);
    }

    .chip.warning {
      color: var(--warning);
      background: rgba(244,183,64,0.08);
      border-color: rgba(244,183,64,0.2);
    }

    .chip.danger {
      color: var(--danger);
      background: rgba(240,93,108,0.08);
      border-color: rgba(240,93,108,0.2);
    }

    .content-grid {
      display: grid;
      grid-template-columns: minmax(0, 1.2fr) minmax(260px, 0.8fr);
      gap: 18px;
      min-height: 420px;
    }

    .card {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: var(--radius-xl);
      box-shadow: var(--shadow);
      overflow: hidden;
    }

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 18px 20px 14px;
      border-bottom: 1px solid var(--border);
    }

    .card-title {
      font-size: 1.02rem;
      font-weight: 700;
      letter-spacing: 0.02em;
    }

    .ghost-btn, .primary-btn, .danger-btn, .secondary-btn {
      border: none;
      padding: 10px 14px;
      border-radius: 10px;
      cursor: pointer;
      font-weight: 700;
      transition: transform 0.15s ease, opacity 0.15s ease;
    }

    .primary-btn {
      color: white;
      background: linear-gradient(135deg, var(--primary), var(--primary-strong));
      box-shadow: 0 8px 18px rgba(77, 163, 255, 0.25);
    }

    .secondary-btn {
      color: var(--text);
      background: rgba(255,255,255,0.04);
      border: 1px solid var(--border);
    }

    .danger-btn {
      color: white;
      background: linear-gradient(135deg, #ff6b6b, var(--danger));
      box-shadow: 0 8px 18px rgba(240, 93, 108, 0.22);
    }

    .ghost-btn {
      color: var(--text-soft);
      background: rgba(255,255,255,0.02);
      border: 1px solid var(--border);
    }

    .primary-btn:hover, .secondary-btn:hover, .ghost-btn:hover, .danger-btn:hover {
      transform: translateY(-1px);
    }

    .chat-panel {
      display: flex;
      flex-direction: column;
      min-height: 420px;
    }

    .chat-box {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 12px;
      padding: 18px 18px 14px;
      background: rgba(8, 17, 31, 0.3);
      min-height: 280px;
      max-height: 440px;
      overflow: auto;
    }

    .message {
      max-width: 88%;
      padding: 12px 14px;
      border-radius: 16px;
      line-height: 1.6;
      font-size: 0.94rem;
      word-break: break-word;
    }

    .message.user {
      align-self: flex-end;
      background: linear-gradient(135deg, rgba(77,163,255,0.2), rgba(90,132,255,0.18));
      border: 1px solid rgba(113,164,255,0.25);
      color: var(--text);
    }

    .message.assistant {
      align-self: flex-start;
      background: rgba(255,255,255,0.04);
      border: 1px solid var(--border);
      color: var(--text-soft);
    }

    .composer {
      display: flex;
      gap: 12px;
      padding: 14px 18px 18px;
      border-top: 1px solid var(--border);
      background: rgba(8, 17, 31, 0.28);
    }

    .composer input {
      flex: 1;
      background: rgba(255,255,255,0.04);
      border: 1px solid var(--border);
      color: var(--text);
      border-radius: 12px;
      padding: 14px 16px;
      outline: none;
    }

    .composer input:focus {
      border-color: rgba(77,163,255,0.7);
      box-shadow: 0 0 0 3px rgba(77,163,255,0.12);
    }

    .filter-row {
      display: flex;
      gap: 10px;
      padding: 12px 18px 0;
      flex-wrap: wrap;
    }

    .filter-row select {
      background: rgba(255,255,255,0.04);
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 8px 10px;
    }

    .alert-list, .ticket-list, .audit-list {
      padding: 14px 18px 18px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .alert-item, .ticket-item, .audit-item {
      display: grid;
      grid-template-columns: 10px minmax(0, 1fr) auto;
      gap: 14px;
      padding: 14px 14px;
      border-radius: 14px;
      background: rgba(255,255,255,0.02);
      border: 1px solid var(--border);
      align-items: center;
    }

    .audit-item {
      display: block;
      padding: 12px 14px;
    }

    .audit-item strong {
      color: var(--text);
      display: block;
      margin-bottom: 4px;
    }

    .audit-item p {
      margin: 0;
      color: var(--text-soft);
      font-size: 0.8rem;
      line-height: 1.6;
    }

    .alert-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--danger);
      box-shadow: 0 0 10px rgba(240,93,108,0.8);
    }

    .alert-dot.warning { background: var(--warning); box-shadow: 0 0 10px rgba(244,183,64,0.8); }
    .alert-dot.success { background: var(--success); box-shadow: 0 0 10px rgba(53,197,138,0.8); }
    .alert-dot.info { background: var(--info); box-shadow: 0 0 10px rgba(92,200,232,0.8); }

    .alert-text h4, .ticket-text h4 {
      margin: 0 0 6px;
      font-size: 0.98rem;
      color: var(--text);
    }

    .alert-text p, .ticket-text p {
      margin: 0;
      color: var(--text-soft);
      line-height: 1.6;
      font-size: 0.82rem;
    }

    .alert-actions {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      justify-content: flex-end;
    }

    .mini-tag {
      padding: 7px 10px;
      border-radius: 999px;
      font-size: 0.72rem;
      font-weight: 700;
      border: 1px solid transparent;
    }

    .mini-tag.level-严重 { background: rgba(240,93,108,0.1); color: var(--danger); border-color: rgba(240,93,108,0.16); }
    .mini-tag.level-重要 { background: rgba(244,183,64,0.1); color: var(--warning); border-color: rgba(244,183,64,0.16); }
    .mini-tag.level-一般 { background: rgba(92,200,232,0.1); color: var(--info); border-color: rgba(92,200,232,0.16); }
    .mini-tag.status-处理中 { background: rgba(77,163,255,0.1); color: var(--primary); border-color: rgba(77,163,255,0.18); }
    .mini-tag.status-已恢复 { background: rgba(53,197,138,0.1); color: var(--success); border-color: rgba(53,197,138,0.18); }
    .mini-tag.status-待处理 { background: rgba(244,183,64,0.1); color: var(--warning); border-color: rgba(244,183,64,0.18); }
    .mini-tag.status-已确认 { background: rgba(92,200,232,0.1); color: var(--info); border-color: rgba(92,200,232,0.18); }

    .side-panel {
      display: flex;
      flex-direction: column;
      gap: 18px;
    }

    .workflow-box {
      padding: 18px;
    }

    .workflow-list {
      display: flex;
      flex-direction: column;
      gap: 14px;
      margin-top: 16px;
    }

    .workflow-step {
      display: grid;
      grid-template-columns: 12px minmax(0, 1fr);
      gap: 12px;
      align-items: flex-start;
    }

    .step-node {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      margin-top: 6px;
      background: rgba(255,255,255,0.24);
      border: 2px solid rgba(255,255,255,0.22);
    }

    .step-node.done { background: var(--success); border-color: rgba(53,197,138,0.5); box-shadow: 0 0 12px rgba(53,197,138,0.6); }
    .step-node.active { background: var(--primary); border-color: rgba(77,163,255,0.5); box-shadow: 0 0 12px rgba(77,163,255,0.7); }
    .step-node.wait { background: var(--warning); border-color: rgba(244,183,64,0.5); box-shadow: 0 0 12px rgba(244,183,64,0.7); }

    .step-text strong {
      display: block;
      margin-bottom: 4px;
      color: var(--text);
      font-size: 0.92rem;
    }

    .step-text span {
      color: var(--text-soft);
      font-size: 0.8rem;
      line-height: 1.4;
    }

    .confirmation-card {
      padding: 18px;
      background: linear-gradient(180deg, rgba(244,183,64,0.06), rgba(240,93,108,0.04));
      border: 1px solid rgba(244,183,64,0.2);
      border-radius: var(--radius-lg);
    }

    .confirmation-card h4 {
      margin: 0 0 10px;
      color: var(--warning);
      font-size: 0.98rem;
    }

    .confirmation-card p {
      color: var(--text-soft);
      font-size: 0.84rem;
      line-height: 1.7;
      margin: 0 0 16px;
    }

    .confirm-actions {
      display: flex;
      gap: 10px;
      margin-top: 12px;
    }

    .confirm-actions button {
      flex: 1;
      min-height: 40px;
    }

    .result-box {
      background: rgba(255,255,255,0.03);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 14px;
      margin: 0 18px 18px;
      color: var(--text-soft);
      line-height: 1.7;
      font-size: 0.87rem;
    }

    .result-box h4 {
      margin: 0 0 10px;
      color: var(--text);
      font-size: 0.96rem;
    }

    .empty-state {
      color: var(--text-muted);
      font-size: 0.85rem;
      padding: 18px;
    }

    @media (max-width: 1200px) {
      .workspace {
        grid-template-columns: 200px minmax(0, 1fr);
      }

      .right-panel {
        grid-column: 1 / -1;
      }

      .metric-row {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }

    @media (max-width: 860px) {
      .workspace {
        grid-template-columns: 1fr;
      }

      .sidebar {
        order: 2;
      }

      .main {
        order: 1;
      }

      .right-panel {
        order: 3;
      }

      .content-grid {
        grid-template-columns: 1fr;
      }

      .metric-row {
        grid-template-columns: 1fr;
      }

      .topbar {
        padding-inline: 16px;
      }
    }
  </style>
</head>
<body>
  <header class="topbar">
    <div class="brand">
      <div class="brand-badge">⚡</div>
      <div class="brand-name">Power Dispatch AI</div>
    </div>
    <div class="topbar-right">
      <div class="status-pill"><span class="status-dot"></span>系统正常</div>
      <span>模型：在线</span>
      <span>演示调度员</span>
    </div>
  </header>

  <div class="workspace">
    <aside class="panel sidebar">
      <a class="nav-item active" href="#"><span class="nav-icon">⌂</span>总览</a>
      <a class="nav-item" href="#"><span class="nav-icon">✦</span>智能助手</a>
      <a class="nav-item" href="#"><span class="nav-icon">⚠</span>告警中心</a>
      <a class="nav-item" href="#"><span class="nav-icon">▣</span>工单中心</a>
      <a class="nav-item" href="#"><span class="nav-icon">⇄</span>运行方式</a>
      <a class="nav-item" href="#"><span class="nav-icon">▤</span>交接班报告</a>
      <a class="nav-item" href="#"><span class="nav-icon">◌</span>审计日志</a>
    </aside>

    <main class="main">
      <section class="metric-row">
        <div class="metric-card">
          <div class="metric-label">严重告警</div>
          <div class="metric-value" id="metricSerious">01</div>
          <div class="metric-foot">
            <span>本日</span>
            <span class="chip danger">● 2% ↑</span>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-label">待确认任务</div>
          <div class="metric-value" id="metricConfirm">03</div>
          <div class="metric-foot">
            <span>工作流</span>
            <span class="chip warning">● 5% ↑</span>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-label">处理中工单</div>
          <div class="metric-value" id="metricTicket">08</div>
          <div class="metric-foot">
            <span>当前</span>
            <span class="chip success">● 正常</span>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-label">系统可用性</div>
          <div class="metric-value">99.9%</div>
          <div class="metric-foot">
            <span>24h</span>
            <span class="chip success">● 稳定</span>
          </div>
        </div>
      </section>

      <section class="content-grid">
        <div class="card chat-panel">
          <div class="card-header">
            <div class="card-title">智能调度助手</div>
            <button class="ghost-btn" type="button" onclick="loadAlerts()">更新告警</button>
          </div>

          <div id="chat" class="chat-box">
            <div class="message assistant">你好，我是电力通信调度智能助手。你可以直接输入：
              “分析当前通信告警”“生成工单草稿”“生成交接班报告”“检查运行方式风险”</div>
          </div>

          <div class="composer">
            <input id="message" placeholder="输入调度指令或故障描述…" />
            <button class="primary-btn" type="button" onclick="sendMessage()">发送</button>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div class="card-title">告警中心</div>
            <button class="secondary-btn" type="button" onclick="loadAlerts()">刷新</button>
          </div>
          <div class="filter-row">
            <select id="alertStation">
              <option value="">全部站点</option>
            </select>
            <select id="alertLevel">
              <option value="">全部等级</option>
              <option value="严重">严重</option>
              <option value="重要">重要</option>
              <option value="一般">一般</option>
            </select>
            <select id="alertStatus">
              <option value="">全部状态</option>
              <option value="处理中">处理中</option>
              <option value="已恢复">已恢复</option>
            </select>
          </div>
          <div class="alert-list" id="alertList"></div>
        </div>
      </section>

      <section class="card" style="margin-top:0;">
        <div class="card-header">
          <div class="card-title">分析结果</div>
          <div class="alert-actions">
            <button class="secondary-btn" type="button" onclick="loadReport()">生成交接班报告</button>
            <button class="primary-btn" type="button" onclick="loadTickets()">刷新工单</button>
          </div>
        </div>
        <div id="resultBox" class="result-box">
          <h4>暂无分析结果</h4>
          <div>请在左侧对话区输入任务描述，AI 将识别当前工作流，并给出建议和人工确认项。</div>
        </div>
      </section>
    </main>

    <aside class="side-panel right-panel">
      <div class="card workflow-box">
        <div class="card-header" style="padding:0 0 12px; border-bottom:1px solid var(--border);">
          <div class="card-title">工作流状态</div>
        </div>
        <div class="workflow-list" id="workflowList">
          <div class="workflow-step">
            <div class="step-node done"></div>
            <div class="step-text"><strong>告警分析</strong><span>已完成，已评估告警影响范围</span></div>
          </div>
          <div class="workflow-step">
            <div class="step-node active"></div>
            <div class="step-text"><strong>风险评估</strong><span>当前正在执行，等待进一步确认</span></div>
          </div>
          <div class="workflow-step">
            <div class="step-node"></div>
            <div class="step-text"><strong>工单草稿</strong><span>待启动</span></div>
          </div>
        </div>
      </div>

      <div class="confirmation-card" id="confirmationCard">
        <h4>人工确认</h4>
        <p>当前存在需要人工确认的步骤：生成故障工单草稿。请确认设备范围、安全措施和影响范围后再继续执行。</p>
        <div class="confirm-actions">
          <button class="ghost-btn" type="button" onclick="declineConfirmation()">拒绝</button>
          <button class="primary-btn" type="button" onclick="confirmCurrentStep()">确认继续</button>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div class="card-title">工单管理</div>
          <button class="secondary-btn" type="button" onclick="loadTickets()">刷新</button>
        </div>
        <div class="ticket-list" id="ticketList"></div>
      </div>

      <div class="card">
        <div class="card-header">
          <div class="card-title">审计日志</div>
          <button class="secondary-btn" type="button" onclick="loadAudit()">刷新</button>
        </div>
        <div class="audit-list" id="auditList"></div>
      </div>
    </aside>
  </div>

  <script>
    const state = { reportText: '', confirmationText: '', workflowContext: null };

    function updateMetricBadges() {
      fetch('/api/alerts')
        .then(r => r.json())
        .then(d => {
          const items = d.items || [];
          const severe = items.filter(item => item.level === '严重').length;
          const pending = items.filter(item => item.status === '处理中').length;
          document.getElementById('metricSerious').textContent = String(severe).padStart(2, '0');
          document.getElementById('metricConfirm').textContent = String(Math.max(1, pending)).padStart(2, '0');
        })
        .catch(() => undefined);

      fetch('/api/tickets')
        .then(r => r.json())
        .then(d => {
          const count = (d.items || []).filter(item => item.status !== '已关闭').length;
          document.getElementById('metricTicket').textContent = String(Math.max(1, count)).padStart(2, '0');
        })
        .catch(() => undefined);
    }

    function getAlertTone(level) {
      if (level === '严重') return 'danger';
      if (level === '重要') return 'warning';
      return 'success';
    }

    function setConfirmationCard(message, show = true) {
      const card = document.getElementById('confirmationCard');
      if (!show) {
        card.style.display = 'none';
        return;
      }
      card.style.display = 'block';
      card.innerHTML = `
        <h4>人工确认</h4>
        <p>${message || '当前存在待确认步骤。请确认后再继续执行。'}</p>
        <div class="confirm-actions">
          <button class="ghost-btn" type="button" onclick="declineConfirmation()">拒绝</button>
          <button class="primary-btn" type="button" onclick="confirmCurrentStep()">确认继续</button>
        </div>
      `;
    }

    function renderWorkflow(steps) {
      const container = document.getElementById('workflowList');
      if (!steps || !steps.length) {
        container.innerHTML = '<div class="empty-state">无当前工作流</div>';
        return;
      }

      const html = steps.map((step, index) => {
        const activeClass = index === 0 ? 'active' : (index === 1 ? 'wait' : '');
        const doneClass = index < 1 ? 'done' : '';
        const nodeClass = doneClass || activeClass || '';
        return `
          <div class="workflow-step">
            <div class="step-node ${nodeClass}"></div>
            <div class="step-text">
              <strong>${step.skill || step.name || '处理步骤'}</strong>
              <span>${step.reason || step.description || '待执行'}</span>
            </div>
          </div>
        `;
      }).join('');

      container.innerHTML = html;
    }

    function renderResult(r) {
      const box = document.getElementById('resultBox');
      let html = `
        <h4>${r.intent || '智能分析'}</h4>
        <div>${r.answer || '暂无说明'}</div>
      `;

      const actions = r.recommended_actions || [];
      if (actions.length) {
        html += '<div style="margin-top:14px; display:flex; flex-wrap:wrap; gap:8px;">';
        actions.forEach(a => {
          html += `<div class="mini-tag" style="display:inline-flex; background:rgba(77,163,255,0.08); color:var(--primary); border-color:rgba(77,163,255,0.16);">${a}</div>`;
        });
        html += '</div>';
      }

      if (r.workflow && r.workflow.length) {
        html += '<div style="margin-top:14px;"><strong>工作流：</strong></div>';
        html += '<div style="margin-top:8px; display:flex; flex-direction:column; gap:8px;">';
        r.workflow.forEach(item => {
          html += `<div style="padding:8px 10px; border-radius:10px; background:rgba(255,255,255,0.03); border:1px solid var(--border); color:var(--text-soft);">${item.skill}：${item.reason || '待执行'}</div>`;
        });
        html += '</div>';
      }

      if (r.ticket_draft) {
        html += `<div style="margin-top:14px;"><strong>工单草稿：</strong></div><pre style="white-space:pre-wrap; margin:10px 0 0; color:var(--text-soft);">${JSON.stringify(r.ticket_draft, null, 2)}</pre>`;
      }

      if (r.need_confirmation) {
        html += `<div style="margin-top:14px; color:var(--warning); font-weight:700;">需要人工确认</div>`;
      }

      box.innerHTML = html;
    }

    function addMessage(type, text) {
      const chat = document.getElementById('chat');
      const div = document.createElement('div');
      div.className = `message ${type}`;
      div.textContent = text;
      chat.appendChild(div);
      chat.scrollTop = chat.scrollHeight;
    }

    async function loadAudit() {
      const res = await fetch('/api/audit/logs');
      const data = await res.json();
      const items = (data.items || []).slice().reverse();
      const list = document.getElementById('auditList');
      if (!items.length) {
        list.innerHTML = '<div class="empty-state">暂无审计记录</div>';
        return;
      }
      list.innerHTML = items.slice(0, 6).map(item => `
        <div class="audit-item">
          <strong>${item.action || '操作'}</strong>
          <p>${item.content || '无详细内容'}</p>
          <p style="margin-top:6px; color:var(--text-muted);">${item.operator || '未知操作员'} · ${item.created_at || ''}</p>
        </div>
      `).join('');
    }

    async function loadAlerts() {
      const station = document.getElementById('alertStation')?.value || '';
      const level = document.getElementById('alertLevel')?.value || '';
      const status = document.getElementById('alertStatus')?.value || '';
      const params = new URLSearchParams();
      if (station) params.set('station', station);
      if (level) params.set('level', level);
      if (status) params.set('status', status);

      const url = '/api/alerts' + (params.toString() ? '?' + params.toString() : '');
      const res = await fetch(url);
      const data = await res.json();
      const items = data.items || [];
      const list = document.getElementById('alertList');

      const stations = [...new Set(items.map(item => item.station).filter(Boolean))];
      const stationSel = document.getElementById('alertStation');
      if (stationSel) {
        stationSel.innerHTML = '<option value="">全部站点</option>' + stations.map(s => `<option value="${s}">${s}</option>`).join('');
      }

      if (!items.length) {
        list.innerHTML = '<div class="empty-state">暂无告警数据</div>';
        return;
      }

      list.innerHTML = items.map(item => `
        <div class="alert-item">
          <div class="alert-dot ${getAlertTone(item.level)}"></div>
          <div class="alert-text">
            <h4>${item.station} / ${item.device}</h4>
            <p>${item.description}</p>
          </div>
          <div class="alert-actions">
            <span class="mini-tag level-${item.level || '一般'}">${item.level || '一般'}</span>
            <span class="mini-tag status-${item.status || '处理中'}">${item.status || '处理中'}</span>
          </div>
        </div>
      `).join('');
    }

    async function loadTickets() {
      const res = await fetch('/api/tickets');
      const data = await res.json();
      const list = document.getElementById('ticketList');
      const items = data.items || [];

      if (!items.length) {
        list.innerHTML = '<div class="empty-state">暂无工单数据</div>';
        return;
      }

      list.innerHTML = items.map(item => `
        <div class="ticket-item">
          <div class="alert-dot ${item.status === '已关闭' ? 'success' : item.status === '待确认' ? 'warning' : 'info'}"></div>
          <div class="ticket-text">
            <h4>${item.title}</h4>
            <p>${item.related_device || '未指定设备'} · ${item.priority || '一般'}</p>
          </div>
          <div class="alert-actions">
            <span class="mini-tag status-${item.status || '处理中'}">${item.status || '处理中'}</span>
          </div>
        </div>
      `).join('');
    }

    async function loadReport() {
      const res = await fetch('/api/reports/handover');
      const data = await res.json();
      state.reportText = `${data.title}\n生成时间：${data.generated_at}\n\n${data.summary}`;
      const box = document.getElementById('resultBox');
      box.innerHTML = `
        <h4>交接班报告</h4>
        <div><strong>概览：</strong>${data.summary || ''}</div>
        <div style="margin-top:12px;"><strong>建议：</strong></div>
        <ul>
          ${(data.recommendations || []).map(item => `<li>${item}</li>`).join('')}
        </ul>
        <div style="margin-top:12px; color:var(--text-soft);">生成时间：${data.generated_at || '---'}</div>
      `;
    }

    async function sendMessage() {
      const input = document.getElementById('message');
      const text = input.value.trim();
      if (!text) return;

      addMessage('user', text);
      input.value = '';

      try {
        const res = await fetch('/api/dispatch/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text, session_id: 'demo-session' })
        });

        const r = await res.json();
        renderResult(r);
        addMessage('assistant', r.answer || '已处理请求。');

        if (r.workflow && r.workflow.length) {
          renderWorkflow(r.workflow);
        } else {
          renderWorkflow([
            { skill: '告警分析', reason: '已完成' },
            { skill: '工单草稿', reason: '待处理' }
          ]);
        }

        if (r.need_confirmation) {
          setConfirmationCard(r.answer || '当前存在待确认步骤。请确认后再继续执行。', true);
          state.confirmationText = r.answer || '当前步骤需要人工确认。';
        } else {
          setConfirmationCard('', false);
        }

        updateMetricBadges();
      } catch (error) {
        addMessage('assistant', '请求失败，请稍后重试。');
      }
    }

    async function confirmCurrentStep() {
      const payload = {
        session_id: 'demo-session',
        action: '确认执行当前步骤',
        content: state.confirmationText || '确认继续当前流程步骤',
        operator: '演示调度员'
      };

      await fetch('/api/audit/confirm', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      addMessage('assistant', '已确认，当前任务已继续执行。');
      setConfirmationCard('', false);
      await loadAlerts();
      await loadTickets();
      await loadAudit();
    }

    function declineConfirmation() {
      const card = document.getElementById('confirmationCard');
      card.innerHTML = `
        <h4>已拒绝</h4>
        <p>当前步骤已停止，建议修改任务描述后重新发起执行。</p>
      `;
      addMessage('assistant', '已拒绝当前步骤。请根据风险提示修改任务后再试。');
    }

    document.getElementById('message').addEventListener('keydown', function (event) {
      if (event.key === 'Enter') {
        sendMessage();
      }
    });

    document.getElementById('alertStation').addEventListener('change', loadAlerts);
    document.getElementById('alertLevel').addEventListener('change', loadAlerts);
    document.getElementById('alertStatus').addEventListener('change', loadAlerts);

    loadAlerts();
    loadTickets();
    loadAudit();
    updateMetricBadges();
  </script>
</body>
</html>
