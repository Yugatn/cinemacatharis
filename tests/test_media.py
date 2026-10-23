import json
import unittest
from unittest.mock import patch, Mock
from cinema_catharsis.media import probe_video

class MediaTests(unittest.TestCase):
    @patch("cinema_catharsis.media.subprocess.run")
    @patch("cinema_catharsis.media.shutil.which", return_value="/usr/bin/ffprobe")
    @patch("cinema_catharsis.media.Path.resolve")
    def test_probe(self, resolve, which, run):
        from pathlib import Path
        resolve.return_value = Path(__file__)
        run.return_value = Mock(returncode=0, stdout=json.dumps({
            "format":{"duration":"12.5","size":"900"},
            "streams":[{"codec_type":"video","codec_name":"h264"}]}))
        result = probe_video("movie.mp4")
        self.assertEqual(result["duration_seconds"], 12.5)
        self.assertEqual(result["streams"][0]["codec_name"], "h264")

    @patch("cinema_catharsis.media.subprocess.run")
    @patch("cinema_catharsis.media.shutil.which", return_value="/usr/bin/ffprobe")
    @patch("cinema_catharsis.media.Path.resolve")
    def test_reject_audio_only(self, resolve, which, run):
        from pathlib import Path
        resolve.return_value = Path(__file__)
        run.return_value = Mock(returncode=0, stdout='{"streams":[{"codec_type":"audio"}]}')
        with self.assertRaises(ValueError):
            probe_video("audio.mp3")
