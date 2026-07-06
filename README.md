# Automated Disk Forensics Framework Using Hybrid Random Forest–LightGBM Model

## Overview

This project presents an automated Windows disk forensic framework that reconstructs forensic timelines and detects anomalous system behavior using a Hybrid Random Forest–LightGBM machine learning model.

The framework automates artifact collection, preprocessing, timeline reconstruction, feature engineering, anomaly detection, visualization, and forensic report generation to reduce manual investigation effort.

---

## Problem Statement

Traditional digital forensic investigations require investigators to manually examine thousands of system artifacts such as:

- Event Logs
- Browser History
- File Metadata
- Registry Entries
- Process Execution Records

Manual analysis is time-consuming and prone to missing suspicious activities.

This project automates the complete forensic workflow using machine learning.

---

## Features

✔ Automated Windows Artifact Collection

✔ Timeline Reconstruction

✔ Feature Engineering

✔ Random Forest Classifier

✔ LightGBM Classifier

✔ Hybrid Soft Voting Ensemble

✔ Automatic Threshold Optimization

✔ Timeline Visualization

✔ Interactive Heatmaps

✔ Automated Report Generation

---

## Workflow

Windows System

↓

Artifact Collection

↓

Data Cleaning

↓

Feature Engineering

↓

Timeline Reconstruction

↓

Hybrid ML Model

↓

Anomaly Detection

↓

Visualization

↓

Forensic Report

---

## Artifacts Collected

- Windows Event Logs
- Prefetch Files
- Browser History
- Registry Information
- File Metadata
- Process Execution Logs
- System Information

---

## Machine Learning Pipeline

Feature Engineering

- Timestamp deviations
- Activity density
- Event frequency
- Process-file correlations
- Time-gap analysis
- Sequence entropy

Models

- Random Forest
- LightGBM
- Hybrid Ensemble

Evaluation

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC

---

## Results

| Model | Accuracy |
|--------|----------|
| Autoencoder | 72.05% |
| Random Forest | 87.37% |
| LightGBM | 88.89% |
| Hybrid RF + LightGBM | **89.73%** |

The Hybrid Random Forest + LightGBM model achieved the best overall performance while reducing false positives and improving anomaly detection accuracy.

---

