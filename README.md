# Hierarchical Federated Learning in Multi-hop Cluster-Based VANETs

The usage of federated learning (FL) in Vehicular Ad hoc Networks (VANET) has garnered significant interest in research due to the advantages of reducing transmission overhead and protecting user privacy by communicating local dataset gradients instead of raw data. However, implementing FL in VANETs faces challenges, including limited communication resources, high vehicle mobility, and the statistical diversity of data distributions. In order to tackle these issues, this paper introduces a novel framework for hierarchical federated learning (HFL) over multi-hop clustering-based VANET. The proposed method utilizes a weighted combination of the average relative speed and cosine similarity of FL model parameters as a clustering metric to consider both data diversity and high vehicle mobility. This metric ensures convergence with minimum changes in cluster heads while tackling the complexities associated with non-independent and identically distributed (non-IID) data scenarios. Additionally, the framework includes a novel mechanism to manage seamless transitions of cluster heads (CHs), followed by transferring the most recent FL model parameter to the designated CH. Alternatively, our approach also considers the option of merging CHs, aiming to reduce their count and, consequently, mitigate associated overhead. Through extensive simulations, the proposed hierarchical federated learning over clustered VANET has been demonstrated to improve accuracy and convergence time significantly while maintaining an acceptable level of packet overhead compared to previously proposed clustering algorithms and non-clustered VANET.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)


## Introduction

Our project focuses on implementing Federated Learning (FL) in Vehicular Ad hoc Networks (VANETs). FL is a machine learning approach that enables collaborative training of models across distributed devices without sharing raw data. In the context of VANETs, where vehicles communicate with each other to improve transportation safety and efficiency, our project aims to leverage FL to disseminate crucial information, such as road conditions and traffic updates, while preserving user privacy.

## Features

- **Implementation of Federated Learning in VANETs:** We bring the power of FL to VANETs, allowing vehicles to collaboratively train machine learning models for improved decision-making on the road.
- **Clustering-based Approach:** Our innovative approach uses multi-hop clustering to form groups of vehicles that collectively train models, ensuring efficient use of communication resources.
- **Dynamic Cluster Head Adaptation:** We introduce a mechanism for seamless transitions of cluster heads, optimizing the convergence of learning models even in the presence of changing vehicle dynamics.
- **Data Diversity and Mobility Consideration:** Our framework integrates both average relative speed and cosine similarity of model parameters, addressing challenges related to data heterogeneity and vehicle mobility.
- **Improved Accuracy and Convergence:** Through extensive simulations, we demonstrate that our approach outperforms previous algorithms, leading to higher accuracy and faster convergence.


```bash
$ git clone https://github.com/SaeedHaghighi/VANETt.git

