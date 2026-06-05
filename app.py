"""
数字人民币智能合约预付卡平台 — 健身房场景 Mockup
启动方式: python gym_smart_contract_app.py
访问地址: http://127.0.0.1:5000
"""
import json
import os
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ---- 模拟智能合约状态 ----
state = {
    "contract_id": "eCNY-SC-20260605-GYM-8842",
    "total_amount": 2000.00,       # 充值总额
    "balance": 1500.00,            # 当前余额（已模拟已消费部分）
    "price_per_session": 50.00,    # 每次扣款
    "total_sessions": 40,          # 总次数
    "used_sessions": 10,           # 已用次数
    "merchant_name": "力美健身房（朝阳店）",
    "merchant_status": "正常经营",
    "transactions": [
        {"date": "2026-06-01", "type": "充值", "amount": 2000.00, "balance": 2000.00, "note": "购买健身年卡 40次"},
        {"date": "2026-06-01", "type": "扣款", "amount": 50.00, "balance": 1950.00, "note": "健身1次"},
        {"date": "2026-06-02", "type": "扣款", "amount": 50.00, "balance": 1900.00, "note": "健身1次"},
        {"date": "2026-06-03", "type": "扣款", "amount": 50.00, "balance": 1850.00, "note": "健身1次"},
        {"date": "2026-06-03", "type": "扣款", "amount": 50.00, "balance": 1800.00, "note": "健身1次"},
        {"date": "2026-06-04", "type": "扣款", "amount": 50.00, "balance": 1750.00, "note": "健身1次"},
        {"date": "2026-06-04", "type": "扣款", "amount": 50.00, "balance": 1700.00, "note": "健身1次"},
        {"date": "2026-06-05", "type": "扣款", "amount": 50.00, "balance": 1650.00, "note": "健身1次"},
        {"date": "2026-06-05", "type": "扣款", "amount": 50.00, "balance": 1600.00, "note": "健身1次"},
        {"date": "2026-06-05", "type": "扣款", "amount": 50.00, "balance": 1550.00, "note": "健身1次"},
        {"date": "2026-06-05", "type": "扣款", "amount": 50.00, "balance": 1500.00, "note": "健身1次"},
    ],
}


@app.route("/")
def index():
    s = dict(state)
    s["remaining_sessions"] = s["total_sessions"] - s["used_sessions"]
    return render_template_string(HTML, state=s, state_json=json.dumps(s, ensure_ascii=False))


@app.route("/api/state")
def get_state():
    s = dict(state)
    s["remaining_sessions"] = s["total_sessions"] - s["used_sessions"]
    return jsonify(s)


@app.route("/api/checkin", methods=["POST"])
def checkin():
    if state["merchant_status"] != "正常经营":
        return jsonify({"ok": False, "msg": "商家已闭店，无法打卡"}), 400

    remaining = state["total_sessions"] - state["used_sessions"]
    if remaining <= 0:
        return jsonify({"ok": False, "msg": "次数已用完，请充值"}), 400

    state["used_sessions"] += 1
    state["balance"] = round(state["balance"] - state["price_per_session"], 2)
    today = datetime.now().strftime("%Y-%m-%d")
    state["transactions"].append({
        "date": today,
        "type": "扣款",
        "amount": state["price_per_session"],
        "balance": state["balance"],
        "note": "健身1次",
    })
    return jsonify({
        "ok": True,
        "balance": state["balance"],
        "used_sessions": state["used_sessions"],
        "remaining_sessions": state["total_sessions"] - state["used_sessions"],
        "transaction": state["transactions"][-1],
    })


@app.route("/api/refund", methods=["POST"])
def refund():
    if state["merchant_status"] == "已闭店（退款中）":
        return jsonify({"ok": False, "msg": "退款已处理，请勿重复操作"}), 400

    remaining = state["total_sessions"] - state["used_sessions"]
    refund_amount = round(remaining * state["price_per_session"], 2)

    state["merchant_status"] = "已闭店（退款中）"
    state["balance"] = 0.0
    today = datetime.now().strftime("%Y-%m-%d")
    state["transactions"].append({
        "date": today,
        "type": "退款",
        "amount": refund_amount,
        "balance": 0.0,
        "note": f"商家闭店，剩余{remaining}次共{refund_amount}元原路退回",
    })
    return jsonify({
        "ok": True,
        "refund_amount": refund_amount,
        "remaining_sessions": remaining,
        "transaction": state["transactions"][-1],
    })


@app.route("/api/reset", methods=["POST"])
def reset():
    """重置演示数据"""
    state["total_amount"] = 2000.00
    state["balance"] = 1500.00
    state["used_sessions"] = 10
    state["merchant_status"] = "正常经营"
    state["transactions"] = [
        {"date": "2026-06-01", "type": "充值", "amount": 2000.00, "balance": 2000.00, "note": "购买健身年卡 40次"},
        {"date": "2026-06-01", "type": "扣款", "amount": 50.00, "balance": 1950.00, "note": "健身1次"},
        {"date": "2026-06-02", "type": "扣款", "amount": 50.00, "balance": 1900.00, "note": "健身1次"},
        {"date": "2026-06-03", "type": "扣款", "amount": 50.00, "balance": 1850.00, "note": "健身1次"},
        {"date": "2026-06-03", "type": "扣款", "amount": 50.00, "balance": 1800.00, "note": "健身1次"},
        {"date": "2026-06-04", "type": "扣款", "amount": 50.00, "balance": 1750.00, "note": "健身1次"},
        {"date": "2026-06-04", "type": "扣款", "amount": 50.00, "balance": 1700.00, "note": "健身1次"},
        {"date": "2026-06-05", "type": "扣款", "amount": 50.00, "balance": 1650.00, "note": "健身1次"},
        {"date": "2026-06-05", "type": "扣款", "amount": 50.00, "balance": 1600.00, "note": "健身1次"},
        {"date": "2026-06-05", "type": "扣款", "amount": 50.00, "balance": 1550.00, "note": "健身1次"},
        {"date": "2026-06-05", "type": "扣款", "amount": 50.00, "balance": 1500.00, "note": "健身1次"},
    ]
    return jsonify({"ok": True})


HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>数字人民币智能合约预付卡平台</title>
<style>
  :root {
    --red: #C41E2A;
    --red-light: #FFF0F1;
    --gold: #B8860B;
    --gold-light: #FFF8E7;
    --bg: #F5F5F5;
    --card: #FFFFFF;
    --text: #1A1A1A;
    --text-secondary: #666;
    --border: #E5E5E5;
    --green: #16A34A;
    --green-light: #F0FDF4;
    --shadow: 0 1px 3px rgba(0,0,0,.08), 0 1px 2px rgba(0,0,0,.06);
    --shadow-lg: 0 4px 12px rgba(0,0,0,.1);
    --radius: 12px;
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    min-height: 100vh;
  }

  /* Header */
  .header {
    background: linear-gradient(135deg, var(--red) 0%, #A01824 100%);
    color: #fff;
    padding: 20px 24px;
    text-align: center;
  }
  .header h1 { font-size: 22px; font-weight: 700; letter-spacing: 1px; }
  .header .subtitle { font-size: 13px; opacity: .85; margin-top: 4px; }

  /* View Toggle Bar */
  .view-toggle-bar {
    display: flex; gap: 0; max-width: 720px; margin: 0 auto; padding: 16px 16px 0;
  }
  .view-toggle-btn {
    flex: 1; padding: 12px 20px; font-size: 15px; font-weight: 700;
    border: 2px solid var(--border); background: #fff; cursor: pointer;
    transition: all .2s; font-family: inherit; text-align: center;
  }
  .view-toggle-btn:first-child { border-radius: 10px 0 0 10px; border-right: none; }
  .view-toggle-btn:last-child { border-radius: 0 10px 10px 0; }
  .view-toggle-btn.consumer-active {
    background: var(--red); color: #fff; border-color: var(--red);
  }
  .view-toggle-btn.merchant-active {
    background: #1A56DB; color: #fff; border-color: #1A56DB;
  }
  .view-toggle-btn .view-badge {
    display: block; font-size: 11px; font-weight: 400; opacity: .8; margin-top: 2px;
  }

  /* Merchant Mode Styles */
  body.merchant-mode .role-card { cursor: default; }
  body.merchant-mode .role-card:hover { border-color: #1A56DB; background: #EFF6FF; }
  body.merchant-mode .role-card.active { border-color: #1A56DB; background: #EFF6FF; }
  body.merchant-mode .section-title { border-left-color: #1A56DB; }

  .btn-locked {
    background: #E5E7EB !important; color: #9CA3AF !important;
    cursor: not-allowed !important; border-color: #D1D5DB !important;
  }
  .btn-locked:hover { background: #E5E7EB !important; }

  /* Security Lock Banner (merchant mode) */
  .merchant-lock-banner {
    display: none; align-items: center; gap: 12px;
    padding: 16px 20px; border-radius: var(--radius);
    background: #EFF6FF; border: 2px dashed #1A56DB;
    color: #1A56DB; font-size: 14px; font-weight: 600;
    margin-bottom: 16px; text-align: center;
  }
  .merchant-lock-banner.show { display: flex; }
  .merchant-lock-banner .lock-icon { font-size: 28px; flex-shrink: 0; }

  /* Security Alert (when merchant clicks locked buttons) */
  .alert-banner {
    background: #FEF2F2; border: 2px solid #FCA5A5; border-radius: var(--radius);
    padding: 16px 20px; margin-bottom: 16px; display: none;
    align-items: flex-start; gap: 12px;
  }
  .alert-banner.show { display: flex; animation: shake .4s ease; }
  .alert-banner .alert-icon { font-size: 28px; flex-shrink: 0; }
  .alert-banner .alert-text strong { display: block; font-size: 14px; color: #991B1B; margin-bottom: 4px; }
  .alert-banner .alert-text span { font-size: 13px; color: #B91C1C; }
  @keyframes shake {
    0%,100% { transform: translateX(0); }
    25% { transform: translateX(-6px); }
    50% { transform: translateX(6px); }
    75% { transform: translateX(-4px); }
  }

  /* Container */
  .container { max-width: 720px; margin: 0 auto; padding: 20px 16px 40px; }

  /* Smart Contract Card */
  .sc-card {
    background: linear-gradient(135deg, #1A1A2E 0%, #16213E 50%, #0F3460 100%);
    border-radius: 16px;
    padding: 24px;
    color: #fff;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-lg);
    margin-bottom: 20px;
  }
  .sc-card::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 140px; height: 140px;
    border-radius: 50%;
    background: rgba(255,255,255,.03);
  }
  .sc-card::after {
    content: '';
    position: absolute;
    bottom: -30px; left: -30px;
    width: 100px; height: 100px;
    border-radius: 50%;
    background: rgba(255,255,255,.03);
  }
  .sc-card .chip {
    display: flex; align-items: center; gap: 8px; margin-bottom: 20px;
    position: relative; z-index: 1;
  }
  .sc-card .chip-icon {
    width: 36px; height: 28px;
    background: linear-gradient(135deg, #FFD700, #FFA500);
    border-radius: 6px;
  }
  .sc-card .chip-label { font-size: 12px; opacity: .7; letter-spacing: 1px; }
  .sc-card .contract-id {
    font-family: "SF Mono", "Cascadia Code", "Consolas", monospace;
    font-size: 13px; opacity: .8; margin-bottom: 16px;
    position: relative; z-index: 1;
    word-break: break-all;
  }
  .sc-card .balance-row {
    display: flex; justify-content: space-between; align-items: flex-end;
    position: relative; z-index: 1;
  }
  .sc-card .balance-label { font-size: 12px; opacity: .7; }
  .sc-card .balance-amount { font-size: 40px; font-weight: 800; letter-spacing: 2px; }
  .sc-card .balance-unit { font-size: 16px; font-weight: 400; opacity: .7; }
  .sc-card .info-row {
    display: flex; gap: 24px; margin-top: 16px;
    position: relative; z-index: 1;
    font-size: 13px; opacity: .8;
  }
  .sc-card .info-row span strong { color: #FFD700; font-weight: 600; }

  .status-badge {
    display: inline-block; padding: 2px 10px; border-radius: 20px;
    font-size: 12px; font-weight: 600;
  }
  .status-badge.normal { background: var(--green-light); color: var(--green); }
  .status-badge.closed { background: var(--red-light); color: var(--red); }

  /* Section Title */
  .section-title {
    font-size: 16px; font-weight: 700; margin: 24px 0 12px;
    padding-left: 12px; border-left: 3px solid var(--red);
  }

  /* Role Cards */
  .role-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 20px; }
  .role-card {
    background: var(--card); border-radius: var(--radius);
    padding: 20px; box-shadow: var(--shadow);
    cursor: pointer; transition: all .2s;
    border: 2px solid transparent;
    text-align: center;
  }
  .role-card:hover { border-color: var(--red); transform: translateY(-1px); box-shadow: var(--shadow-lg); }
  .role-card.active { border-color: var(--red); background: var(--red-light); }
  .role-card .role-icon { font-size: 32px; margin-bottom: 8px; }
  .role-card .role-name { font-size: 15px; font-weight: 700; margin-bottom: 4px; }
  .role-card .role-desc { font-size: 12px; color: var(--text-secondary); }

  /* Action Panel */
  .action-panel {
    background: var(--card); border-radius: var(--radius);
    padding: 24px; box-shadow: var(--shadow);
    margin-bottom: 20px;
    display: none;
  }
  .action-panel.visible { display: block; }

  .btn {
    display: inline-flex; align-items: center; justify-content: center; gap: 6px;
    padding: 12px 28px; border-radius: 8px; font-size: 15px; font-weight: 600;
    border: none; cursor: pointer; transition: all .2s;
    font-family: inherit;
  }
  .btn:active { transform: scale(.97); }
  .btn-primary { background: var(--red); color: #fff; width: 100%; }
  .btn-primary:hover { background: #A01824; }
  .btn-outline {
    background: #fff; color: var(--red); border: 2px solid var(--red);
    width: 100%;
  }
  .btn-outline:hover { background: var(--red-light); }
  .btn:disabled { opacity: .5; cursor: not-allowed; }

  /* Transaction Table */
  .tx-table { width: 100%; border-collapse: collapse; font-size: 13px; }
  .tx-table th {
    text-align: left; padding: 10px 8px; border-bottom: 2px solid var(--border);
    font-size: 12px; color: var(--text-secondary); font-weight: 600;
  }
  .tx-table td { padding: 10px 8px; border-bottom: 1px solid var(--border); }
  .tx-table .tx-deduct { color: var(--red); font-weight: 600; }
  .tx-table .tx-recharge { color: var(--green); font-weight: 600; }
  .tx-table .tx-refund { color: #2563EB; font-weight: 600; }
  .tx-scroll { max-height: 360px; overflow-y: auto; }

  /* Toast */
  .toast {
    position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
    padding: 12px 24px; border-radius: 8px; font-size: 14px; font-weight: 600;
    z-index: 999; box-shadow: var(--shadow-lg);
    animation: slideDown .3s ease;
    display: none;
  }
  .toast.show { display: block; }
  .toast.success { background: var(--green); color: #fff; }
  .toast.error { background: var(--red); color: #fff; }
  @keyframes slideDown { from { opacity:0; transform:translateX(-50%) translateY(-20px); } to { opacity:1; transform:translateX(-50%) translateY(0); } }

  /* Security Banner */
  .security-banner {
    background: linear-gradient(135deg, var(--gold-light), #FFF4D6);
    border: 1px solid #F0D060; border-radius: var(--radius);
    padding: 20px 24px; display: flex; align-items: flex-start; gap: 14px;
  }
  .security-banner .shield { font-size: 36px; flex-shrink: 0; }
  .security-banner h3 { font-size: 15px; font-weight: 700; color: var(--gold); margin-bottom: 6px; }
  .security-banner p { font-size: 13px; color: #8B6914; line-height: 1.7; }

  /* Refund Summary */
  .refund-summary {
    background: var(--green-light); border-radius: var(--radius);
    padding: 20px; margin: 16px 0; text-align: center;
    display: none;
  }
  .refund-summary.show { display: block; }
  .refund-summary .amount { font-size: 36px; font-weight: 800; color: var(--green); }
  .refund-summary .detail { font-size: 13px; color: var(--text-secondary); margin-top: 4px; }

  .reset-btn {
    display: block; margin: 32px auto 0; padding: 8px 20px;
    background: none; border: 1px dashed #CCC; border-radius: 6px;
    color: #999; font-size: 12px; cursor: pointer; font-family: inherit;
  }
  .reset-btn:hover { border-color: #999; color: #666; }

  @media (max-width: 480px) {
    .role-grid { grid-template-columns: 1fr; }
    .sc-card .balance-amount { font-size: 32px; }
    .sc-card .info-row { flex-direction: column; gap: 4px; }
  }
</style>
</head>
<body>

<div class="header">
  <h1>数字人民币智能合约预付卡平台</h1>
  <div class="subtitle">e-CNY Smart Contract · 预付资金托管 · 一课一结</div>
</div>

<!-- 视角切换栏 -->
<div class="view-toggle-bar">
  <button class="view-toggle-btn consumer-active" id="btnConsumerView" onclick="switchView('consumer')">
    👤 消费者视角<div class="view-badge">可操作：打卡 · 退款</div>
  </button>
  <button class="view-toggle-btn" id="btnMerchantView" onclick="switchView('merchant')">
    🏪 商家视角<div class="view-badge">只读：查账 · 对账</div>
  </button>
</div>

<div class="container">

  <!-- 智能合约卡片 -->
  <div class="sc-card">
    <div class="chip">
      <div class="chip-icon"></div>
      <div class="chip-label">e-CNY SMART CONTRACT</div>
    </div>
    <div class="contract-id" id="contractId">合约编号：{{ state.contract_id }}</div>
    <div class="balance-row">
      <div>
        <div class="balance-label">合约账户余额</div>
        <div class="balance-amount">¥<span id="balance">{{ "%.2f" % state.balance }}</span></div>
      </div>
      <div class="balance-unit">元</div>
    </div>
    <div class="info-row">
      <span>已用 <strong id="usedSessions">{{ state.used_sessions }}</strong> 次</span>
      <span>剩余 <strong id="remainingSessions">{{ state.total_sessions - state.used_sessions }}</strong> 次</span>
      <span>商户：<strong>{{ state.merchant_name }}</strong></span>
      <span id="merchantStatus">
        {% if state.merchant_status == '正常经营' %}
        <span class="status-badge normal">● 正常经营</span>
        {% else %}
        <span class="status-badge closed">● {{ state.merchant_status }}</span>
        {% endif %}
      </span>
    </div>
  </div>

  <!-- 角色选择 -->
  <div class="section-title">选择演示角色</div>
  <div class="role-grid">
    <div class="role-card active" data-role="recharge" onclick="switchRole('recharge', this)">
      <div class="role-icon">💰</div>
      <div class="role-name">充值员面</div>
      <div class="role-desc">充值2000元 → 智能合约托管</div>
    </div>
    <div class="role-card" data-role="record" onclick="switchRole('record', this)">
      <div class="role-icon">📋</div>
      <div class="role-name">消费记录员面</div>
      <div class="role-desc">每次打卡自动扣款 50 元</div>
    </div>
    <div class="role-card" data-role="refund" onclick="switchRole('refund', this)">
      <div class="role-icon">↩️</div>
      <div class="role-name">退款员面</div>
      <div class="role-desc">一键退款 · 原路返回</div>
    </div>
    <div class="role-card" data-role="security" onclick="switchRole('security', this)">
      <div class="role-icon">🛡️</div>
      <div class="role-name">安全提示</div>
      <div class="role-desc">央行托管 · 资金安全</div>
    </div>
  </div>

  <!-- ===== 充值员面 ===== -->
  <div class="action-panel visible" id="panel-recharge">
    <div class="merchant-lock-banner" id="lockBannerRecharge">
      <span class="lock-icon">🔒</span> 商家视角 · 无权操作资金
    </div>
    <h3 style="margin-bottom:16px">💰 充值演示</h3>
    <div style="background:var(--gold-light);border-radius:10px;padding:16px;margin-bottom:16px">
      <div style="font-size:14px;color:#8B6914;line-height:1.8">
        <strong>充值流程：</strong><br>
        1. 用户支付 <strong>2000 元</strong> 购买健身年卡（40次，50元/次）<br>
        2. 资金 <strong>不进入</strong> 商家账户，直接锁定在数字人民币智能合约<br>
        3. 每次到店打卡 → 智能合约自动执行扣款 → 资金划转给商家<br>
        4. 未消费的资金 <strong>始终由央行系统托管</strong>，商家无法提前挪用
      </div>
    </div>
    <button class="btn btn-outline" onclick="switchRole('record', document.querySelector('[data-role=record]'))">
      👆 点击"打卡"按钮模拟每次到店消费
    </button>
  </div>

  <!-- ===== 消费记录员面 ===== -->
  <div class="action-panel" id="panel-record">
    <div class="merchant-lock-banner" id="lockBannerRecord">
      <span class="lock-icon">🔒</span> 商家视角 · 无权操作打卡扣款
    </div>
    <div class="alert-banner" id="alertBannerRecord">
      <span class="alert-icon">🚫</span>
      <div class="alert-text">
        <strong>操作被拦截：商家无权执行打卡扣款</strong>
        <span>资金由央行数字人民币系统托管，只有消费者到店打卡才能触发智能合约自动扣款，商家无法主动划转资金。</span>
      </div>
    </div>
    <h3 style="margin-bottom:12px">📋 到店打卡 · 自动扣款</h3>
    <button class="btn btn-primary" id="btnCheckin" onclick="doCheckin()">
      🏋️ 打卡（健身1次 · 扣款 ¥50.00）
    </button>
    <div id="checkinResult" style="margin-top:12px;font-size:14px;text-align:center;color:var(--green);display:none"></div>

    <h4 style="margin:20px 0 8px;font-size:14px;color:var(--text-secondary)">📜 消费记录</h4>
    <div class="tx-scroll">
      <table class="tx-table" id="txTable">
        <thead><tr><th>日期</th><th>类型</th><th>金额</th><th>余额</th><th>备注</th></tr></thead>
        <tbody></tbody>
      </table>
    </div>
  </div>

  <!-- ===== 退款员面 ===== -->
  <div class="action-panel" id="panel-refund">
    <div class="merchant-lock-banner" id="lockBannerRefund">
      <span class="lock-icon">🔒</span> 商家视角 · 无权操作退款
    </div>
    <div class="alert-banner" id="alertBannerRefund">
      <span class="alert-icon">🚫</span>
      <div class="alert-text">
        <strong>操作被拦截：商家无权发起退款</strong>
        <span>退款由智能合约自动执行，只有消费者有权发起。剩余资金由央行系统核算后原路退回，商家无法干预退款流程。</span>
      </div>
    </div>
    <h3 style="margin-bottom:12px">↩️ 一键退款</h3>
    <div style="font-size:14px;color:var(--text-secondary);margin-bottom:16px;line-height:1.8">
      模拟场景：<strong>商家突然闭店</strong>，用户申请退款。<br>
      智能合约自动核算剩余次数和金额，<strong>原路退回</strong>到用户数字钱包。
    </div>
    <div class="refund-summary" id="refundSummary">
      <div style="font-size:14px;color:var(--text-secondary)">退款金额</div>
      <div class="amount" id="refundAmount">¥0.00</div>
      <div class="detail" id="refundDetail"></div>
    </div>
    <button class="btn btn-primary" id="btnRefund" onclick="doRefund()" style="background:#2563EB">
      ⚡ 一键发起退款（模拟商家闭店）
    </button>
  </div>

  <!-- ===== 安全提示 ===== -->
  <div class="action-panel" id="panel-security">
    <h3 style="margin-bottom:12px">🛡️ 安全说明</h3>
    <div class="security-banner">
      <div class="shield">🛡️</div>
      <div>
        <h3>资金由央行数字人民币系统托管，商家无法挪用</h3>
        <p>
          ✓ <strong>资金托管：</strong>预付资金锁定在央行数字人民币智能合约中，不在商家账户<br>
          ✓ <strong>一课一结：</strong>用户每次到店消费后，合约自动执行扣款，资金才划转给商家<br>
          ✓ <strong>实时可查：</strong>每一笔资金变动均在区块链上存证，用户可随时查询<br>
          ✓ <strong>原路退回：</strong>商家闭店或用户申请退款，剩余资金自动核算、原路退回<br>
          ✓ <strong>智能合约不可篡改：</strong>扣款规则一经部署不可单方修改，杜绝商家跑路风险
        </p>
      </div>
    </div>
  </div>

</div>

<button class="reset-btn" onclick="doReset()">↻ 重置演示数据</button>

<div class="toast" id="toast"></div>

<script>
// ---- 状态 ----
let st = {{ state_json | safe }};
let currentView = 'consumer'; // 'consumer' | 'merchant'

function switchView(view) {
  currentView = view;
  const btnC = document.getElementById('btnConsumerView');
  const btnM = document.getElementById('btnMerchantView');

  if (view === 'consumer') {
    document.body.classList.remove('merchant-mode');
    btnC.className = 'view-toggle-btn consumer-active';
    btnM.className = 'view-toggle-btn';
    // 隐藏所有 alert banners
    document.querySelectorAll('.alert-banner').forEach(b => b.classList.remove('show'));
  } else {
    document.body.classList.add('merchant-mode');
    btnC.className = 'view-toggle-btn';
    btnM.className = 'view-toggle-btn merchant-active';
  }
  updateLockBanners();
  updateButtons();
  updateRoleCards();
}

function updateLockBanners() {
  const isMerchant = currentView === 'merchant';
  ['lockBannerRecharge', 'lockBannerRecord', 'lockBannerRefund'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.classList.toggle('show', isMerchant);
  });
}

function updateRoleCards() {
  // In merchant mode, role cards that involve money ops show locked icons
  document.querySelectorAll('.role-card').forEach(card => {
    const role = card.dataset.role;
    if (currentView === 'merchant' && (role === 'recharge' || role === 'refund')) {
      card.querySelector('.role-icon').textContent = '🔒';
    } else if (role === 'recharge') {
      card.querySelector('.role-icon').textContent = '💰';
    } else if (role === 'refund') {
      card.querySelector('.role-icon').textContent = '↩️';
    } else if (role === 'record') {
      card.querySelector('.role-icon').textContent = '📋';
    } else if (role === 'security') {
      card.querySelector('.role-icon').textContent = '🛡️';
    }
  });
}

async function refreshUI() {
  const resp = await fetch('/api/state');
  st = await resp.json();
  document.getElementById('balance').textContent = st.balance.toFixed(2);
  document.getElementById('usedSessions').textContent = st.used_sessions;
  document.getElementById('remainingSessions').textContent = st.remaining_sessions;

  const badge = st.merchant_status === '正常经营'
    ? '<span class="status-badge normal">● 正常经营</span>'
    : '<span class="status-badge closed">● ' + st.merchant_status + '</span>';
  document.getElementById('merchantStatus').innerHTML = badge;

  renderTransactions();
  updateButtons();
  updateLockBanners();
}

function renderTransactions() {
  const tbody = document.querySelector('#txTable tbody');
  const txs = [...st.transactions].reverse();
  tbody.innerHTML = txs.map(tx => {
    let cls = '';
    if (tx.type === '扣款') cls = 'tx-deduct';
    else if (tx.type === '充值') cls = 'tx-recharge';
    else if (tx.type === '退款') cls = 'tx-refund';
    const sign = tx.type === '退款' ? '+' : (tx.type === '充值' ? '+' : '-');
    return `<tr>
      <td>${tx.date}</td>
      <td>${tx.type}</td>
      <td class="${cls}">${sign}¥${tx.amount.toFixed(2)}</td>
      <td>¥${tx.balance.toFixed(2)}</td>
      <td>${tx.note}</td>
    </tr>`;
  }).join('');
}

function updateButtons() {
  const btnCheckin = document.getElementById('btnCheckin');
  const btnRefund = document.getElementById('btnRefund');

  if (currentView === 'merchant') {
    btnCheckin.disabled = true;
    btnCheckin.className = 'btn btn-locked';
    btnCheckin.textContent = '🔒 无权操作：资金由央行托管';
    btnCheckin.style.width = '100%';
    btnRefund.disabled = true;
    btnRefund.className = 'btn btn-locked';
    btnRefund.textContent = '🔒 无权操作：资金由央行托管';
    btnRefund.style.width = '100%';
    return;
  }

  // Consumer mode
  btnCheckin.className = 'btn btn-primary';
  btnRefund.className = 'btn btn-primary';
  btnRefund.style.background = '#2563EB';
  if (st.merchant_status !== '正常经营') {
    btnCheckin.disabled = true;
    btnCheckin.textContent = '商家已闭店，无法打卡';
    btnRefund.disabled = true;
    btnRefund.textContent = '退款已完成';
  } else if (st.remaining_sessions <= 0) {
    btnCheckin.disabled = true;
    btnCheckin.textContent = '次数已用完';
    btnRefund.disabled = false;
    btnRefund.textContent = '⚡ 一键发起退款（模拟商家闭店）';
  } else {
    btnCheckin.disabled = false;
    btnCheckin.textContent = '🏋️ 打卡（健身1次 · 扣款 ¥50.00）';
    btnRefund.disabled = false;
    btnRefund.textContent = '⚡ 一键发起退款（模拟商家闭店）';
  }
}

function switchRole(role, el) {
  // In merchant mode, money-op cards show alert instead of switching
  if (currentView === 'merchant' && (role === 'recharge' || role === 'refund')) {
    showToast('商家无权操作资金，资金由央行托管', 'error');
    // flash the relevant alert if panel is open
    if (role === 'refund') {
      const banner = document.getElementById('alertBannerRefund');
      banner.classList.add('show');
      setTimeout(() => banner.classList.remove('show'), 3000);
    }
    return;
  }

  document.querySelectorAll('.role-card').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
  document.querySelectorAll('.action-panel').forEach(p => p.classList.remove('visible'));
  document.getElementById('panel-' + role).classList.add('visible');

  // Hide alert banners when switching panels
  document.querySelectorAll('.alert-banner').forEach(b => b.classList.remove('show'));
}

async function doCheckin() {
  if (currentView === 'merchant') {
    const banner = document.getElementById('alertBannerRecord');
    banner.classList.add('show');
    setTimeout(() => banner.classList.remove('show'), 3000);
    showToast('操作被拦截：商家无权打卡扣款', 'error');
    return;
  }

  const resp = await fetch('/api/checkin', { method: 'POST' });
  const data = await resp.json();
  if (data.ok) {
    const today = new Date().toISOString().slice(0, 10);
    const result = document.getElementById('checkinResult');
    result.style.display = 'block';
    result.innerHTML = `✅ ${today} 健身1次，扣款 ¥50.00，剩余 ¥${data.balance.toFixed(2)}（${data.remaining_sessions}次）`;
    await refreshUI();
    showToast('打卡成功！已自动扣款 ¥50.00', 'success');
  } else {
    showToast(data.msg, 'error');
  }
}

async function doRefund() {
  if (currentView === 'merchant') {
    const banner = document.getElementById('alertBannerRefund');
    banner.classList.add('show');
    setTimeout(() => banner.classList.remove('show'), 3000);
    showToast('操作被拦截：商家无权发起退款', 'error');
    return;
  }

  if (!confirm('确认模拟"商家闭店"并一键退款？\n\n系统将自动核算剩余次数和金额，原路退回。')) return;

  const resp = await fetch('/api/refund', { method: 'POST' });
  const data = await resp.json();
  if (data.ok) {
    document.getElementById('refundAmount').textContent = '¥' + data.refund_amount.toFixed(2);
    document.getElementById('refundDetail').textContent =
      '剩余 ' + data.remaining_sessions + ' 次 × ¥50.00 = ¥' + data.refund_amount.toFixed(2) + ' 已原路退回';
    document.getElementById('refundSummary').classList.add('show');
    await refreshUI();
    showToast('退款成功！¥' + data.refund_amount.toFixed(2) + ' 已原路退回', 'success');
  } else {
    showToast(data.msg, 'error');
  }
}

async function doReset() {
  await fetch('/api/reset', { method: 'POST' });
  document.getElementById('refundSummary').classList.remove('show');
  document.getElementById('checkinResult').style.display = 'none';
  document.querySelectorAll('.alert-banner').forEach(b => b.classList.remove('show'));
  switchRole('recharge', document.querySelector('[data-role=recharge]'));
  await refreshUI();
  showToast('已重置演示数据', 'success');
}

function showToast(msg, type) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = 'toast ' + type + ' show';
  clearTimeout(t._tid);
  t._tid = setTimeout(() => t.classList.remove('show'), 2500);
}

// 初始渲染
switchView('consumer');
refreshUI();
</script>
</body>
</html>"""


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("\n  数字人民币智能合约预付卡平台")
    print("  ==============================")
    print(f"  访问地址: http://127.0.0.1:{port}\n")
    app.run(debug=False, host="0.0.0.0", port=port)
