# RAG 知识库问答项目简历改写方案

说明：以下内容基于当前项目代码落地情况整理，未将 RAGAS、Cross-Encoder 重排写成已实现核心能力。性能数值为可替换占位值，后续建议用真实压测结果覆盖。

## 方案一：后端/RAG 工程导向

**项目名称：企业级 RAG 知识库问答平台**

**项目介绍：** 面向企业私有文档检索难、知识复用成本高的问题，设计并实现支持文档入库、向量检索、多轮问答和引用溯源的 RAG 问答平台；通过 FastAPI 构建后端服务，结合 LangChain、向量数据库和对象存储，形成从文档解析到问答生成的完整闭环。

**技术栈：** FastAPI、LangChain、SQLAlchemy、Alembic、MySQL、MinIO、ChromaDB/Qdrant、OpenAI/DeepSeek/Ollama、Docker Compose、Nginx、Next.js、TypeScript、Tailwind CSS、Vercel AI SDK

**核心实现：**

- **异步入库：** 针对大文件上传和向量化耗时阻塞问题，使用 MinIO 临时存储 + FastAPI BackgroundTasks + 任务状态轮询实现异步处理，接口上传响应控制在 300ms 内，支持 100MB 级文件入库。
- **增量更新：** 针对重复上传和文档更新导致重复 embedding 的问题，使用文件 SHA-256 与 chunk hash 进行去重和变更检测，重复文件跳过处理，重复向量化成本降低 80%+。
- **多轮检索：** 针对连续追问中问题上下文缺失的问题，基于 LangChain history-aware retriever 重写用户问题后再检索，Top-3 召回准确率提升至 90%+。
- **引用溯源：** 针对 LLM 回答不可验证的问题，将检索上下文编码后随流式响应返回，前端解析为 citation 弹窗，支持句级引用查看，答案可追溯率达到 100%。
- **服务解耦：** 针对模型和向量库切换成本高的问题，抽象 LLM、Embedding、VectorStore 工厂层，支持 OpenAI/DeepSeek/Ollama 与 ChromaDB/Qdrant 配置化切换，新增 provider 改动控制在 1 个工厂类内。

## 方案二：AI 应用/算法工程导向

**项目名称：私有知识库 RAG 问答系统**

**项目介绍：** 为解决企业私有知识分散、人工检索效率低的问题，构建基于 RAG 的知识库问答系统；系统将 PDF、DOCX、Markdown、TXT 等文档解析分块后写入向量库，并在对话时结合历史上下文检索相关片段生成带引用答案。

**技术栈：** LangChain、RecursiveCharacterTextSplitter、OpenAI Embeddings、DashScope/Ollama Embeddings、ChromaDB、Qdrant、FastAPI、MySQL、MinIO、Vercel AI SDK、React Markdown

**核心实现：**

- **文档解析：** 针对多格式文档无法统一入库的问题，封装 PDF/DOCX/MD/TXT 加载器和可配置 chunk size、overlap 分块策略，单文档可稳定生成 1000+ 文本块。
- **向量召回：** 针对传统关键词搜索语义匹配弱的问题，使用 Embedding + Chroma/Qdrant 进行相似度检索，Top-K 可配置为 1/3/5/10，检索延迟控制在 200ms 内。
- **追问改写：** 针对多轮对话中“它/这个”等指代不清的问题，使用 LangChain history-aware retriever 将历史消息压入问题改写链路，连续追问命中率提升 30%+。
- **上下文组装：** 针对大模型幻觉和无关回答问题，通过检索上下文约束 Prompt，并要求按 `[citation:x]` 输出引用，回答相关性提升至 90%+。
- **效果调试：** 针对检索质量不可观测的问题，实现检索测试页面，支持输入 query、Top-K 并展示 score 与来源文档，检索问题定位效率提升 60%+。

## 方案三：全栈产品闭环导向

**项目名称：可溯源知识库 AI 问答平台**

**项目介绍：** 面向个人和团队私有知识库问答场景，开发覆盖知识库管理、文档上传、分块预览、异步入库、流式问答和 API 调用的全栈系统；通过前后端分离架构提升系统可维护性，并用引用溯源增强回答可信度。

**技术栈：** Next.js 14、TypeScript、shadcn/Radix UI、Tailwind CSS、Vercel AI SDK、FastAPI、JWT、API Key、LangChain、MySQL、MinIO、ChromaDB、Docker Compose

**核心实现：**

- **上传流程：** 针对文档入库过程不可控的问题，设计“上传-预览-处理”三步流程，前端支持拖拽上传、分块参数配置和任务进度展示，处理状态每 2s 自动轮询。
- **流式问答：** 针对长答案等待时间长的问题，使用 Vercel AI SDK + FastAPI StreamingResponse 实现 token 级流式输出，首字响应控制在 1.5s 内。
- **引用交互：** 针对用户难以验证答案来源的问题，前端解析后端返回的 Base64 上下文并渲染 citation 弹窗，支持查看原文片段、文件名和知识库信息。
- **权限隔离：** 针对多用户数据隔离问题，基于 JWT 校验用户身份，并在知识库、聊天、文档接口中按 user_id 过滤，避免跨用户访问。
- **开放接口：** 针对外部系统集成需求，实现 API Key 管理和 `/openapi/knowledge/{id}/query` 查询接口，支持程序化检索私有知识库。

## 方案四：平台架构/工程化导向

**项目名称：可扩展 RAG 问答服务平台**

**项目介绍：** 为降低私有知识库 AI 问答系统的接入和扩展成本，搭建可配置的 RAG 服务平台；后端抽象模型、嵌入和向量库适配层，前端提供知识库管理和检索测试能力，支持本地和云端模型灵活部署。

**技术栈：** FastAPI、Pydantic、SQLAlchemy、Alembic、MySQL、MinIO、LangChain、ChromaDB/Qdrant、OpenAI/DeepSeek/Ollama/DashScope、Docker、Nginx

**核心实现：**

- **工厂抽象：** 针对模型和向量数据库耦合问题，设计 LLMFactory、EmbeddingsFactory、VectorStoreFactory，支持多 provider 配置化切换，扩展新后端无需改动业务路由。
- **存储分层：** 针对文件、元数据和向量混存难维护的问题，使用 MinIO 存原始文档、MySQL 存任务和 chunk 元数据、Chroma/Qdrant 存向量，实现存储职责拆分。
- **任务治理：** 针对批量文档处理失败难追踪的问题，设计 ProcessingTask 状态表，覆盖 pending、processing、completed、failed 状态，失败原因可回传前端。
- **部署编排：** 针对多服务启动复杂的问题，使用 Docker Compose 编排前端、后端、MySQL、ChromaDB、MinIO、Nginx，支持一键启动，健康检查通过率 99%+。
- **资源清理：** 针对删除知识库后的脏数据问题，删除时联动清理 MinIO 对象、向量集合和数据库记录，存储残留降低至 0。

## 方案五：秋招精简高密度版

**项目名称：RAG 私有知识库问答平台**

**项目介绍：** 基于企业私有文档问答场景，实现支持多格式文档入库、语义检索、多轮问答、引用溯源和开放 API 的 RAG 平台；负责后端核心链路、向量检索、异步文档处理及前端问答交互。

**技术栈：** FastAPI、LangChain、MySQL、SQLAlchemy、MinIO、ChromaDB/Qdrant、OpenAI/DeepSeek/Ollama、Next.js、TypeScript、Docker、Nginx

**核心实现：**

- **异步处理：** 针对文档解析和 embedding 耗时问题，使用后台任务 + 任务表 + 前端轮询解耦上传与处理，上传接口响应控制在 300ms 内。
- **分块去重：** 针对重复上传和增量更新问题，使用 SHA-256 计算文件和 chunk 指纹，重复文档直接跳过，重复 embedding 成本降低 80%+。
- **语义检索：** 针对关键词检索召回不足问题，基于 Embedding 和 Chroma/Qdrant 实现 Top-K 相似度检索，Top-3 召回准确率达到 90%+。
- **多轮问答：** 针对上下文追问语义缺失问题，使用 history-aware retriever 改写问题并组装上下文，回答相关性提升 30%+。
- **引用溯源：** 针对回答可信度不足问题，将检索片段随流式回答返回并在前端渲染引用弹窗，答案来源可追溯率达到 100%。

## 默认取舍

- 推荐优先使用方案五投递通用后端/AI 应用岗位，长度更适合简历一栏。
- 若岗位偏 AI 工程，用方案二；偏全栈，用方案三；偏后端平台，用方案一或方案四。
- 性能指标目前按简历占位口径写入，建议后续至少补测：上传接口耗时、文档处理吞吐、Top-K 检索延迟、流式首字时间、重复上传跳过率。
