# -*- coding: utf-8 -*-
"""
tests/test_arabic_nlp.py — Arapça NLP, Kök Harf Korumalı Telaffuz Değerlendirici (نَحْلَة vs رحلة),
Ardışık Tekrar Tekilleştirici (نحلة نحلة -> نحلة), Evrensel Mahreç & Vezin/Med Koçu,
Sözlük Varyant (/) Eşleştirici, Pedagojik Hareke Rehberi ve SM-2 Otomatik Birim Test Paketi (v38).

Çalıştırmak için proje ana dizininde:
    py tests/test_arabic_nlp.py
"""

import os
import sys
import datetime
import unittest

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists(os.path.join(PROJECT_ROOT, "core")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if __name__ == "__main__":
    _venv_python = os.path.join(PROJECT_ROOT, ".venv", "Scripts", "python.exe")
    if os.path.exists(_venv_python) and os.path.normcase(sys.executable) != os.path.normcase(_venv_python):
        import subprocess
        sys.exit(subprocess.call([_venv_python] + sys.argv))

from core.arabic_nlp import (
    remove_diacritics,
    has_arabic_diacritics,
    sanitize_arabic_sentence,
    sanitize_turkish_sentence,
    expand_arabic_variants,
    check_item_quality,
    normalize_arabic,
    _phonetic_skeleton,
    collapse_consecutive_repeats,
    compare_arabic,
    evaluate_sentence_words,
    analyze_phoneme_and_makhraj_errors,
    build_haraka_guide,
    estimate_word_cefr,
    estimate_sentence_cefr,
    estimate_dialogue_cefr,
    shape_arabic,
    MAX_WIN32_SAFE_CODEPOINTS
)
from core.database import _compute_sm2_schedule
from core.dictionary import classify_dictionary_category_and_emoji


class TestArabicNLPAndCoach(unittest.TestCase):
    """Arapça metin işleme, kök harf koruması, ardışık tekrar tekilleştirme, mahreç koçu ve SM-2 testleri."""

    def test_01_diacritics_detection_and_removal(self):
        word_harakeli = "مُعَلِّمٌ"
        word_harekesiz = "معلم"
        self.assertTrue(has_arabic_diacritics(word_harakeli))
        self.assertFalse(has_arabic_diacritics(word_harekesiz))
        self.assertEqual(remove_diacritics(word_harakeli), word_harekesiz)

    def test_02_text_doctor_sanitization(self):
        dirty_ar = "ذَهَبَ أَحْمَدُ (22) إِلَى الْمَدْرَسَةِ (11.30) مبكراً ."
        clean_ar = sanitize_arabic_sentence(dirty_ar)
        self.assertNotIn("(22)", clean_ar)
        self.assertNotIn("(11.30)", clean_ar)
        self.assertTrue(clean_ar.endswith("مبكراً."))

        dirty_tr = "Yazarın üslubu oldukça etkileyicidir. 81"
        clean_tr = sanitize_turkish_sentence(dirty_tr)
        self.assertEqual(clean_tr, "Yazarın üslubu oldukça etkileyicidir.")

    def test_03_arabic_comparison_and_word_evaluation(self):
        score, _, _ = compare_arabic("اَلْكِتَابُ", "كتاب")
        self.assertGreaterEqual(score, 0.95)

        exp_sent = "ذَهَبَ الطَّالِبُ إِلَى الْمَكْتَبَةِ"
        heard_sent = "ذهب الطالب الى المكتبه"
        word_res, ratio = evaluate_sentence_words(exp_sent, heard_sent)
        self.assertEqual(len(word_res), 4)
        self.assertEqual(ratio, 1.0)
        self.assertTrue(all(is_ok for _, is_ok in word_res))

    def test_04_makhraj_and_phoneme_coach(self):
        tips_sad = analyze_phoneme_and_makhraj_errors("صَبَاحُ الْخَيْرِ", "سباح الخير")
        self.assertTrue(any("ص ➔ س" in t["title"] for t in tips_sad))

        tips_ayn = analyze_phoneme_and_makhraj_errors("عَلِيمٌ", "أليم")
        self.assertTrue(any("ع ➔ ا" in t["title"] or "Ayn" in t["title"] for t in tips_ayn))

        tips_zal = analyze_phoneme_and_makhraj_errors("ذَهَبَ", "زهب")
        self.assertTrue(any("ذ ➔ ز" in t["title"] for t in tips_zal))

        tips_med = analyze_phoneme_and_makhraj_errors("قَالَ", "قل")
        self.assertTrue(any("Med" in t["title"] or "Uzatma" in t["title"] for t in tips_med))

    def test_05_cefr_estimation_morphology_and_phrases(self):
        self.assertEqual(estimate_word_cefr("اَلسَّلَامُ عَلَيْكُمْ"), "A1")
        self.assertEqual(estimate_sentence_cefr("اَلْحَمْدُ لِلّٰهِ رَبِّ الْعَالَمِينَ"), "A1")

        self.assertEqual(estimate_word_cefr("كِتَابٌ", gorsel="kitap.png"), "A1")
        self.assertEqual(estimate_word_cefr("تُفَّاحَةٌ", gorsel="elma.png"), "A1")

        lvl_complex = estimate_word_cefr("اِسْتِقْلَالِيَّةٌ")
        self.assertIn(lvl_complex, ("B2", "C1"))

        c1_sentence = (
            "انْطِلَاقاً مِنْ هَذَا الْمَبْدَأِ وَبِمُوجِبِ الْقَوَانِينِ الدَّوْلِيَّةِ لَاسِيَّمَا مَا يَتَعَلَّقُ "
            "بِحِمَايَةِ الْبِيئَةِ وَالتَّنْمِيَةِ الْمُسْتَدَامَةِ فِي الْمُجْتَمَعَاتِ الْحَدِيثَةِ."
        )
        self.assertEqual(estimate_sentence_cefr(c1_sentence), "C1")

        dlg_a1 = ["مَرْحَباً.", "أَهْلاً وَسَهْلاً، كَيْفَ حَالُكَ؟", "أَنَا بِخَيْرٍ، شُكْراً."]
        self.assertEqual(estimate_dialogue_cefr(dlg_a1), "A1")

    def test_06_sm2_spaced_repetition_schedule(self):
        today_iso = datetime.date.today().isoformat()

        iv1, ef1, next1 = _compute_sm2_schedule(0, 2.5, is_correct=True)
        self.assertEqual(iv1, 1)
        self.assertGreater(ef1, 2.5)
        self.assertGreater(next1, today_iso)

        iv2, ef2, _ = _compute_sm2_schedule(iv1, ef1, is_correct=True)
        self.assertEqual(iv2, 3)

        iv3, ef3, _ = _compute_sm2_schedule(iv2, ef2, is_correct=True)
        self.assertGreaterEqual(iv3, 7)

        iv_fail, ef_fail, next_fail = _compute_sm2_schedule(iv3, ef3, is_correct=False)
        self.assertEqual(iv_fail, 1)
        self.assertLess(ef_fail, ef3)
        self.assertEqual(next_fail, today_iso)

    def test_07_rtl_shaping_and_quality_audit(self):
        long_ar = " ".join(["كَلِمَةٌ"] * 25)
        shaped = shape_arabic(long_ar, max_chars_per_line=45)
        lines = shaped.splitlines()
        self.assertGreater(len(lines), 1)
        for ln in lines:
            self.assertTrue(ln.startswith("\u200f"))
            clean_ln = ln.replace("\u200f", "")
            self.assertLessEqual(len(clean_ln), MAX_WIN32_SAFE_CODEPOINTS)

        issues = check_item_quality("w1", "كتاب", "")
        self.assertTrue(any("Hareke" in i for i in issues))
        self.assertTrue(any("Türkçe" in i for i in issues))

    def test_08_dictionary_slash_variants(self):
        raw_entry = "سَلَامَة / سَلَام"
        variants = expand_arabic_variants(raw_entry)
        self.assertIn("سَلَامَة", variants)
        self.assertIn("سَلَام", variants)

        sc1, _, _ = compare_arabic(raw_entry, "سلام")
        sc2, _, _ = compare_arabic(raw_entry, "سلامة")
        self.assertEqual(sc1, 1.0)
        self.assertEqual(sc2, 1.0)

        w_res, ratio = evaluate_sentence_words("مَرْكَزُ تَسَوُّقٍ / مَوْل", "مول")
        self.assertEqual(ratio, 1.0)
        self.assertEqual(len(w_res), 1)

    def test_09_false_positive_med_filter_and_haraka_guide(self):
        tips_beyt = analyze_phoneme_and_makhraj_errors("بَيْت", "بات")
        self.assertTrue(any("Vezin / Med Harfi Değişimi" in t["title"] for t in tips_beyt))
        self.assertFalse(any("Gereksiz Uzatma" in t["title"] for t in tips_beyt))

        tips_diff = analyze_phoneme_and_makhraj_errors("قَالَ", "كتب")
        self.assertFalse(any("Med (Uzatma) Eksikliği" in t["title"] for t in tips_diff))

        guide = build_haraka_guide("كَتَبَ")
        self.assertIn("Fetha", guide)

    def test_10_dictionary_auto_category_and_emoji(self):
        cat_id1, _, emoji1 = classify_dictionary_category_and_emoji("doktor, hekim", "isim")
        self.assertEqual(cat_id1, "szl_saglik")
        self.assertEqual(emoji1, "🏥")

        cat_id2, _, emoji2 = classify_dictionary_category_and_emoji("uçak, havalimanı", "isim")
        self.assertEqual(cat_id2, "szl_seyahat")
        self.assertEqual(emoji2, "✈️")

        cat_id3, _, emoji3 = classify_dictionary_category_and_emoji("ders çalışmak, öğrenim görmek", "fiil")
        self.assertEqual(cat_id3, "szl_egitim")
        self.assertEqual(emoji3, "🎓")

    def test_11_root_consonant_mismatch_nahla_rihla(self):
        """نَحْلَة (Arı) yerine رحلة (Yolculuk) denildiğinde kesinlikle yanlış sayılmalı ve ن ➔ ر yakalanmalı."""
        score, _, _ = compare_arabic("نَحْلَة", "رحلة")
        self.assertLess(score, 0.65, f"نَحْلَة vs رحلة puanı 0.65'in altında olmalıydı, çıkan: {score}")

        word_res, ratio = evaluate_sentence_words("نَحْلَة", "رحلة")
        self.assertEqual(ratio, 0.0)
        self.assertFalse(word_res[0][1])

        tips = analyze_phoneme_and_makhraj_errors("نَحْلَة", "رحلة")
        self.assertTrue(len(tips) >= 1, "نَحْلَة vs رحلة için mahreç/kök uyarısı üretilmeliydi!")
        self.assertTrue(any("ن ➔ ر" in t["title"] for t in tips), f"ن ➔ ر uyarısı bulunamadı: {tips}")

    def test_12_makhraj_false_positive_guard_kitab_amil(self):
        """كِتَاب vs كتب ve عَامِل vs عمل med hatası değil, Sarf Kalıbı / Vezin Farklılığı olarak raporlanmalı."""
        tips_kitab = analyze_phoneme_and_makhraj_errors("كِتَاب", "كتب")
        self.assertFalse(any("Med (Uzatma) Eksikliği" in t["title"] for t in tips_kitab))
        self.assertTrue(any("Vezin Farklılığı" in t["title"] for t in tips_kitab))

        tips_amil = analyze_phoneme_and_makhraj_errors("عَامِل", "عمل")
        self.assertFalse(any("Med (Uzatma) Eksikliği" in t["title"] for t in tips_amil))
        self.assertTrue(any("Vezin Farklılığı" in t["title"] for t in tips_amil))

        tips_qala = analyze_phoneme_and_makhraj_errors("قَالَ", "قل")
        self.assertTrue(any("Med (Uzatma) Eksikliği" in t["title"] for t in tips_qala))

    def test_13_normalize_and_phonetic_skeleton_consistency(self):
        """_phonetic_skeleton ve normalize_arabic 'ة -> ه' dönüşümünde tam tutarlı olmalı."""
        for word in ["مَدْرَسَة", "نَحْلَة", "كِتَاب", "قَلَم"]:
            ph = _phonetic_skeleton(word)
            nr = normalize_arabic(word)
            self.assertNotIn("ة", ph, f"_phonetic_skeleton 'ة' içeriyor: {word}")
            self.assertEqual(ph, nr)

    def test_14_short_word_and_universal_consonant_protection(self):
        """Kısa med'siz kelimelerde med uyarısı çıkmamalı; listede olmayan harf değişimleri de yakalanmalı."""
        tips_short = analyze_phoneme_and_makhraj_errors("قَلَ", "قل")
        self.assertFalse(any("Med" in t["title"] for t in tips_short))

        tips_univ = analyze_phoneme_and_makhraj_errors("بَيْت", "ليت")
        self.assertTrue(any("ب ➔ ل" in t["title"] for t in tips_univ))

    def test_15_consecutive_word_repeat_deduplication(self):
        """Öğrencinin kelimeyi peş peşe iki kez okuması ('نحلة نحلة') doğru kabul edilmeli."""
        self.assertEqual(collapse_consecutive_repeats("نحلة نحلة"), "نحلة")
        sc, _, _ = compare_arabic("نَحْلَة", "نحلة نحلة")
        self.assertEqual(sc, 1.0)
        _, ratio = evaluate_sentence_words("نَحْلَة", "نحلة نحلة")
        self.assertEqual(ratio, 1.0)
        tips = analyze_phoneme_and_makhraj_errors("نَحْلَة", "نحلة نحلة")
        self.assertEqual(len(tips), 0)


if __name__ == "__main__":
    print("=" * 72)
    print("🧪 ARAPÇA TELAFFUZ VE KONUŞMA ASİSTANI — OTOMATİK BİRİM TESTLERİ (v38)")
    print("=" * 72)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestArabicNLPAndCoach)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    print("=" * 72)
    if result.wasSuccessful():
        print(f"✅ TÜM TESTLER BAŞARIYLA GEÇTİ! ({result.testsRun}/{result.testsRun})")
        sys.exit(0)
    else:
        print(f"❌ BAZI TESTLER BAŞARISIZ OLDU! (Hata: {len(result.failures) + len(result.errors)})")
        sys.exit(1)