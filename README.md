## How to Run

### Run LLMHalSpot and Baselines

**One-model mode**:

```commandline
cd src
sh main_one_model.sh
```

**Two-model mode**:

```commandline
cd src
sh main_two_models.sh
```

**Baseline**: direct ask, CoT, and Self-Consistency

```commandline
cd src
sh main_self_validation.sh
```

Remember: Before running the above commands, you have to re-check the commands in the shell files. Otherwise, the unnecessary token cost may be caused by improper run (with wrong options)

### Generate diagrams and histograms

First, we need to label the ground truth after executing the following command:

```commandline
cd src
sh statistics_one_model.sh
```

After examining the `xxx_relabel_all.json` in `log/hal_spot`, store the ground-truth in the file named `xxx_ground_truth_all.json`.

Then you can generate the diagrams and histograms as follows:

**For LLMHalSpot (one-model mode):**

```commandline
cd src/statistics
python3 check_ablation.py
```

**For LLMHalSpot (two-model mode):**

```commandline
cd src/statistics
python3 check_two_model_mode.py
```

**For Baseline:**

```commandline
cd src/statistics
python3 check_self_verification.py
```

**Token Cost of LLMHalSpot**

```commandline
cd src/statistics
python3 check_token_cost.py
```

All the diagrams and histograms are stored in `src/statistics`.

## Cost

- Self-Consistency (K = 5, t = 0.5)

  - GPT-4: $42 (estimated)
 
  - GPT-3.5: $6.08

  - Claude-3-haiku: $12.17

  - Gemini: Free

  - Total: $108.9
  
- Directly Ask + CoT (K = 1, t = 0)

  - GPT-4: $36.4

  - GPT-3.5: $4.35

  - Claude-3-haiku: $5.9

  - Gemini: Free
 
  - Total: $46.68

- Initial Inference: $46.68

- Total cost for one track: $242.26


