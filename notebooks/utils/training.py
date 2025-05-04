"""
Training utilities for the drum transcription model.
"""
import torch
import torch.nn.functional as F
from tqdm.notebook import tqdm
from pathlib import Path


def combined_loss_function(
    onset_logits,
    velocity_pred,
    onset_target,
    velocity_target,
    onset_weight=0.8,
    positive_weight=10.0
):
    """
    Combined loss for both onset detection and velocity prediction.

    Args:
        onset_logits: Raw logits for onset predictions [B, n_drums, T]
        velocity_pred: Velocity predictions [B, n_drums, T]
        onset_target: Onset targets [B, n_drums, T]
        velocity_target: Velocity targets [B, n_drums, T]
        onset_weight: Weight for onset loss (velocity_weight = 1 - onset_weight)
        positive_weight: Weight for positive examples in BCE loss

    Returns:
        Tuple of (combined_loss, onset_loss, velocity_loss)
    """
    onset_target = onset_target.float()

    # Create weight tensor with high values for positive examples
    weights = torch.ones_like(onset_target, device=onset_logits.device)
    weights[onset_target > 0.5] = positive_weight

    # Use binary_cross_entropy_with_logits
    onset_loss = F.binary_cross_entropy_with_logits(
        onset_logits,
        onset_target,
        weight=weights
    )

    # Only compute velocity loss where drums are hit
    mask = onset_target > 0.5
    if mask.sum() > 0:
        velocity_loss = F.mse_loss(
            velocity_pred[mask], velocity_target.float()[mask])
    else:
        velocity_loss = torch.tensor(
            0.0, device=onset_logits.device, dtype=torch.float32)

    # Weighted combination
    velocity_weight = 1.0 - onset_weight
    combined = onset_weight * onset_loss + velocity_weight * velocity_loss

    return combined, onset_loss, velocity_loss
