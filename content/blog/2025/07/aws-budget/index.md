+++
title = "AWS Budget設定ガイド - 個人AWSアカウントのコスト管理"
description = "個人AWSアカウントのコスト管理を効率的に行うためのAWS Budget設定ガイド。月額数ドルの利用でも予期しない請求を防ぐため、ゼロ支出予算、月次全体予算、サービス別予算の3層構造で監視する実践的な設定方法を紹介。CloudFormation、CLI、Terraformを使った具体的な実装例付き。"
date = 2025-07-05
aliases = ["/articles/2025/07/05/aws-budget"]

[taxonomies]
tags = ["Tech", "AWS"]
[extra]
social_media_card = "ogp.webp"
+++

<details>
<summary>Table of Contents</summary>
<!-- toc -->
</details>

個人AWSアカウントのコスト管理を効率的に行うためのAWS Budget設定ガイド。月額数ドルの利用でも予期しない請求を防ぐため、ゼロ支出予算、月次全体予算、サービス別予算の3層構造で監視する実践的な設定方法を紹介。CloudFormation、CLI、Terraformを使った具体的な実装例付き。

## 1. AWS Budgetとは

AWS Budgetsは、AWSの利用料金を監視し、設定した予算を超えそうな場合や超えた場
合にアラートを送信するサービスです。

主な機能は、次のようなものです。

- **コスト予算**: 実際の費用や予測費用を監視
- **使用量予算**: サービスの使用量を監視
- **リザーブドインスタンス（RI）予算**: RIの利用率を監視
- **Savings Plans予算**: Savings Plansの利用率を監視

AWS Budgetを使うことで、
コストの異常を早期発見しアラートを上げることで、
予期しない請求を防ぐことが可能となります。
AWS Budgetを利用することで支出を計画的に管理できるようになります。

AWS Budgetでは「予算」という形でアラートのルールを作成しますが、
最大20,000個の予算を無料で作成可能です。

## 2. 私の場合のBudgetルールの考え方

### 私のAWS利用状況

私のAWSの利用状況は以下のようなものです。

1. 複数のブログをAmplifyで運営
   - 静的サイトジェネレーターを使用したブログサイト
   - 記事更新時のビルド・デプロイでコストが発生
   - 更新頻度により月額コストが変動

2. Amplifyとは別に複数のブログをS3のホスティング機能で運営
   - 静的なHTMLサイトをS3で直接ホスティング
   - CloudFront経由での配信
   - アクセス数とデータ転送量でコストが変動

3. ドローンやアクションカメラの動画バックアップ
   - 高解像度動画ファイルをS3に保存
   - ストレージ容量が累積的に増加
   - S3コスト急増の要因となりやすい

### コスト分析結果

他のサービスからAWS主体の運営に変更したのが年初です
過去6ヶ月のコスト実績を分析すると以下のようになります。

- 月平均: $2.54
- 最高月額: $4.96（3月）
- 最低月額: $0.07（1月）

サービス別総コストコストに分析すると、次の通りです。

1. Amplify: $16.42（変動が大きい）
   - ブログ更新頻度による変動
   - 新規ブログ立ち上げ時のビルド増加
2. **S3**: $2.89（6月に急増）
   - 動画バックアップによる累積的増加
   - 静的サイトホスティングのデータ転送
3. **その他**: 少額

### Budget設計方針

1. **全体予算**: 過去最高額の150%程度で設定（余裕を持たせる）
2. **サービス別予算**: 変動の大きいサービスを個別管理
3. **ゼロ支出予算**: 未使用サービスの不正利用を検知
4. **アラート設定**: 80%と100%の2段階（50%は省略してアラート疲れを防ぐ）

## 3. 実際の設定内容

### 3.1 ゼロ支出予算（未使用サービス監視）

**基本設定**

- 予算名: UnusedServices-ZeroSpend
- 予算額: $0.01
- 期間: 月次
- 対象サービス: KMS, Secrets Manager, SNSなど

**CLI設定**

```bash
aws budgets create-budget \
  --account-id <ACCOUNT_ID> \
  --budget file://zero-spend-budget.json \
  --notifications-with-subscribers file://notifications.json
```

**zero-spend-budget.json**

```json
{
  "BudgetName": "UnusedServices-ZeroSpend",
  "BudgetLimit": {
    "Amount": "0.01",
    "Unit": "USD"
  },
  "TimeUnit": "MONTHLY",
  "BudgetType": "COST",
  "CostFilters": {
    "Service": [
      "AWS Key Management Service",
      "AWS Secrets Manager",
      "Amazon Simple Notification Service",
      "Amazon Simple Queue Service",
      "AmazonCloudWatch"
    ]
  }
}
```

### 3.2 月次全体予算

**基本設定**

- 予算名: Monthly-Total-Budget
- 予算額: $7.00
- 期間: 月次
- アラート: 80%、100%、100%予測

**CloudFormationテンプレート**

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: "AWS Budget Configuration"

Resources:
  MonthlyTotalBudget:
    Type: AWS::Budgets::Budget
    Properties:
      Budget:
        BudgetName: Monthly-Total-Budget
        BudgetLimit:
          Amount: 7.0
          Unit: USD
        TimeUnit: MONTHLY
        BudgetType: COST
      NotificationsWithSubscribers:
        - Notification:
            NotificationType: ACTUAL
            ComparisonOperator: GREATER_THAN
            Threshold: 80
            ThresholdType: PERCENTAGE
          Subscribers:
            - SubscriptionType: EMAIL
              Address: your-email@example.com
        - Notification:
            NotificationType: ACTUAL
            ComparisonOperator: GREATER_THAN
            Threshold: 100
            ThresholdType: PERCENTAGE
          Subscribers:
            - SubscriptionType: EMAIL
              Address: your-email@example.com
        - Notification:
            NotificationType: FORECASTED
            ComparisonOperator: GREATER_THAN
            Threshold: 100
            ThresholdType: PERCENTAGE
          Subscribers:
            - SubscriptionType: EMAIL
              Address: your-email@example.com
```

### 3.3 Amplify予算

**基本設定**

- 予算名: Amplify-Monthly-Budget
- 予算額: $3.50
- 期間: 月次
- アラート: 50%、80%、100%、100%予測

**CLI設定**

```bash
aws budgets create-budget \
  --account-id <ACCOUNT_ID> \
  --budget '{
    "BudgetName": "Amplify-Monthly-Budget",
    "BudgetLimit": {
      "Amount": "3.50",
      "Unit": "USD"
    },
    "TimeUnit": "MONTHLY",
    "BudgetType": "COST",
    "CostFilters": {
      "Service": ["AWS Amplify"]
    }
  }' \
  --notifications-with-subscribers '[
    {
      "Notification": {
        "NotificationType": "ACTUAL",
        "ComparisonOperator": "GREATER_THAN",
        "Threshold": 50,
        "ThresholdType": "PERCENTAGE"
      },
      "Subscribers": [{
        "SubscriptionType": "EMAIL",
        "Address": "your-email@example.com"
      }]
    }
  ]'
```

### 3.4 S3予算

**基本設定**

- 予算名: S3-Storage-Monitor
- 予算額: $2.00
- 期間: 月次
- アラート: 50%、80%、100%、100%予測

**Terraform設定**

```hcl
resource "aws_budgets_budget" "s3_budget" {
  name         = "S3-Storage-Monitor"
  budget_type  = "COST"
  limit_amount = "2.0"
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  cost_filter {
    name = "Service"
    values = ["Amazon Simple Storage Service"]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type            = "PERCENTAGE"
    notification_type         = "ACTUAL"
    subscriber_email_addresses = ["your-email@example.com"]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type            = "PERCENTAGE"
    notification_type         = "FORECASTED"
    subscriber_email_addresses = ["your-email@example.com"]
  }
}
```

## 今後の改善ポイント

金額的にはわずかですが、次のようなこともやってよいかなと思っています。

1. Cost Anomaly Detectionの設定
   - 機械学習による異常検知
   - 前月比50%以上の増加で自動通知

2. タグベースの予算管理
   - 環境別（dev/prod）のタグ付け
   - プロジェクト別のコスト追跡

3. 四半期・年間予算の追加
   - 長期的なコスト管理
   - 年間$80程度を想定

4. 自動アクションの設定
   - 予算超過時の非本番環境の自動停止
   - Lambda関数によるコスト最適化

5. S3ライフサイクルポリシー(既に実施)
   - 古い動画ファイルをGlacierへ移行
   - アクセス頻度の低いコンテンツのコスト最適化

## 参考リンク

- [AWS Budgets ドキュメント](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html)
- [AWS CLI Budgets リファレンス](https://docs.aws.amazon.com/cli/latest/reference/budgets/index.html)
- [CloudFormation Budgets リソース](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-budgets-budget.html)
