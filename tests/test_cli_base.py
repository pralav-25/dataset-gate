from dataset_gate.cli import main


def test_help(capsys):
    assert main([]) == 0
    assert "Check data" in capsys.readouterr().out
