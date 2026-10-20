import pytest
from app.adapters.provider_factory import get_llm_adapter
from app.adapters.nvidia_adapter import NvidiaAdapter
from app.services.voice_service import VoiceService
from app.services.notification_service import NotificationService

@pytest.mark.asyncio
async def test_nvidia_adapter_instantiation_and_fallback():
    """Verify NVIDIA NIM adapter fallback works without throwing errors."""
    adapter = get_llm_adapter("nvidia")
    assert isinstance(adapter, NvidiaAdapter)
    
    # Run test generation with fallback
    res = await adapter.generate("Test prompt")
    assert len(res) > 0

@pytest.mark.asyncio
async def test_voice_service_transcription():
    """Verify voice transcription service returns valid transcription."""
    res = await VoiceService.transcribe_audio_bytes(b"dummy_wav_header_bytes")
    assert res["success"] is True
    assert "transcription" in res or "status" in res

@pytest.mark.asyncio
async def test_notification_service():
    """Verify notification dispatch creates valid audit structure."""
    res = await NotificationService.dispatch_workflow_audit_email(
        workflow_id="wf_test_123",
        objective="Find best laptop under ₹70,000",
        status="COMPLETED",
        total_latency_ms=145,
        calibrated_trust=0.96
    )
    assert "dispatched" in res
