# AI2-THOR 任务规划系统

基于 [AI2-THOR](https://ai2thor.allenai.org/) 模拟器的家居机器人任务规划毕业设计项目。

机器人在虚拟家居场景中自主完成：**找到目标物体 → 拾取 → 导航到目标容器 → 放置**。

---

## 功能特性

- **规则式任务规划**：通过状态机驱动的任务规划器，依次完成搜索、拾取、导航、放置
- **A\* 路径规划**：基于 AI2-THOR 可达位置图自动生成最短路径，将路径转换为具体导航动作
- **容器搜索策略**：自动开启/关闭抽屉、柜门，记录已搜索容器避免重复
- **实验框架**：支持多轮重复实验，自动统计成功率与平均步数
- **结果可视化**：将实验指标绘制为图表并保存

---

## 项目结构

```
ai2thor_task_planning/
├── main.py                    # 主入口，运行单次任务
├── config.py                  # 全局配置（场景、目标物体、步长等）
│
├── env/
│   ├── controller.py          # AI2-THOR 控制器封装
│   └── scene_manager.py       # 场景重置与随机化
│
├── perception/
│   └── object_detector.py     # 基于模拟器元数据的目标检测
│
├── planning/
│   ├── task_planner.py        # 高层任务规划器（集成 A*）
│   └── path_planner.py        # A* 路径规划算法
│
├── execution/
│   └── action_executor.py     # 动作序列执行器
│
├── experiments/
│   ├── run_experiments.py     # 多轮实验运行框架
│   └── metrics.py             # 指标收集与统计
│
└── utils/
    └── visualization.py       # 实验结果可视化
```

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

> Windows 用户若遇到 `ai2thor` 安装问题，建议使用 Python 3.10，并确保已安装 Visual C++ 运行库。

### 2. 修改配置（可选）

编辑 `config.py` 调整场景和任务目标：

```python
SCENE            = "FloorPlan1"   # AI2-THOR 场景名
TARGET_OBJECT    = "Apple"        # 要拾取的目标物体类型
GOAL_RECEPTACLE  = "Drawer"       # 目标放置容器类型
GRID_SIZE        = 0.25           # 导航网格分辨率（米）
MAX_STEPS        = 200            # 每阶段最大步数
STEP_DELAY       = 0.5            # 动作间隔（秒），0 为最快
```

### 3. 运行单次任务

```bash
python main.py
```

执行完成后会在当前目录保存 `final_scene.png`（任务结束时的场景截图）。

### 4. 运行多轮实验

```bash
python experiments/run_experiments.py
```

会输出成功率、平均步数，并生成 `success_rate.png` 和 `steps.png` 图表。

---

## 核心模块说明

### A\* 路径规划（`planning/path_planner.py`）

| 方法 | 说明 |
|------|------|
| `search(start, goal, reachable_set)` | 在可达格子集合上执行 A\* 搜索 |
| `reconstruct_path(came_from, start, goal)` | 从搜索结果重建路径列表 |
| `world_to_grid(x, z)` | 世界坐标 → 网格坐标 |
| `build_reachable_set(positions)` | 构建可达格子集合 |
| `path_to_actions(path, start_rotation)` | 路径 → AI2-THOR 动作序列 |

### 任务规划器（`planning/task_planner.py`）

- `plan_find_object()`：搜索目标物体，可见且距离 > 1.5m 时触发 A\* 导航，到达后执行拾取
- `plan_place()`：导航至目标容器，距离 > 1.5m 时触发 A\* 导航，到位后执行放置
- `plan_open_cabinet()`：开启场景中第一个可开启的容器

---

## 依赖环境

| 依赖 | 版本要求 | 用途 |
|------|----------|------|
| ai2thor | ≥ 5.0.0 | 3D 家居模拟器 |
| numpy | ≥ 1.24.0 | 数组计算 |
| opencv-python | ≥ 4.8.0 | 图像保存 |
| matplotlib | ≥ 3.7.0 | 实验结果可视化 |

---

## 许可证

本项目为毕业设计学习用途，仅供参考。
