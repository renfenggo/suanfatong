#!/usr/bin/env python3
import json

c = json.load(open('data/stage3f_batch4_full49_dependency_cleanup_plan.json', 'r', encoding='utf-8'))
p = json.load(open('data/stage3f_batch4_full49_candidate_plan_v2.json', 'r', encoding='utf-8'))
d = json.load(open('data/stage3f_batch4_full49_dynamic_precheck_v2.json', 'r', encoding='utf-8'))

print('=== dependency_cleanup_plan.json ===')
print('  dep_cleanup_required:', c['dependency_cleanup_required'])
print('  total_candidates:', c['summary']['total_candidates'])
print('  section_id_refs_found:', c['summary']['section_id_refs_found'])
print('  dangling_refs_found:', c['summary']['dangling_refs_found'])
print('  dep_cycles_found:', c['summary']['dependency_cycles_found'])

print()
print('=== candidate_plan_v2.json ===')
print('  candidates count:', len(p['candidates']))
print('  recommendation:', p['recommendation'])
print('  recommended_merge_count:', p['recommended_merge_count'])
print('  dependency_cleanup_required:', p['dependency_cleanup_required'])
print('  dependency_mapping_risk:', p['dependency_mapping_risk'])
print('  section_ref_dependencies:', p['section_ref_dependencies'])
print('  candidate_dependency_cycle:', p['candidate_dependency_cycle'])
print('  needs_new_section:', p['needs_new_section'])
print('  excluded_duplicate:', len(p['excluded_duplicate_or_near_duplicate']))
print('  excluded_merged:', len(p['excluded_already_merged_candidates']))
print('  manual_review_count:', p['summary']['manual_review_count'])
print('  main_graph_modified:', p['meta']['main_graph_modified'])
print('  dep_cleanup_applied:', p['summary']['dependency_cleanup_applied'])

for c2 in p['candidates']:
    if c2['mapping_confidence'] == 'medium':
        print('    medium:', c2['candidate_id'], '(', c2['name'], ') manual_review=', c2['manual_review_required'])

print()
print('=== dynamic_precheck_v2.json ===')
print('  recommendation:', d['recommendation'])
print('  recommended_merge_count:', d['recommended_merge_count'])
print('  main_graph_modified:', d['meta']['main_graph_modified'])
print('  validate_only_passed:', d['meta']['validate_only_passed'])
print('  dep_cleanup_completed:', d['meta']['dependency_cleanup_completed'])
print('  summary:', json.dumps(d['precheck_results']['summary']))

print()
print('=== ALL CHECKS ===')
all_ok = True
checks = [
    ('recommendation == ready_for_1号线程_merge_full49', p['recommendation'] == 'ready_for_1号线程_merge_full49'),
    ('recommended_merge_count == 49', p['recommended_merge_count'] == 49),
    ('dependency_cleanup_required == false', p['dependency_cleanup_required'] == False),
    ('dependency_mapping_risk == []', p['dependency_mapping_risk'] == []),
    ('section_ref_dependencies == []', p['section_ref_dependencies'] == []),
    ('candidate_dependency_cycle == false', p['candidate_dependency_cycle'] == False),
    ('needs_new_section == false', p['needs_new_section'] == False),
    ('excluded_duplicate is empty', len(p['excluded_duplicate_or_near_duplicate']) == 0),
    ('excluded_merged is empty', len(p['excluded_already_merged_candidates']) == 0),
    ('main_graph_modified == false', p['meta']['main_graph_modified'] == False),
    ('candidates count == 49', len(p['candidates']) == 49),
    ('section_id_refs == 0', c['summary']['section_id_refs_found'] == 0),
    ('dangling_refs == 0', c['summary']['dangling_refs_found'] == 0),
    ('dep_cycles == 0', c['summary']['dependency_cycles_found'] == 0),
    ('dep_cleanup_required in cleanup_plan', c['dependency_cleanup_required'] == False),
    ('v2_precheck recommendation correct', d['recommendation'] == 'ready_for_1号线程_merge_full49'),
    ('validate_only_passed == true', d['meta']['validate_only_passed'] == True),
]
for name, ok in checks:
    status = 'PASS' if ok else 'FAIL'
    if not ok:
        all_ok = False
    print(f'  [{status}] {name}')

print()
if all_ok:
    print('>>> ALL CHECKS PASSED <<<')
else:
    print('>>> SOME CHECKS FAILED <<<')
