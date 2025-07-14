#!/usr/bin/env sage

def test_automorphism_group_computation():
    """
    Test automorphism group computation for all major SageMath group types.
    Returns a comprehensive report of which group types work.
    """
    results = {
        'working': [],
        'failing': [],
        'partial': [],
        'unknown': []
    }
    
    test_cases = [
        # Finite groups
        ("CyclicGroup(6)", lambda: CyclicGroup(6)),
        ("CyclicGroup(12)", lambda: CyclicGroup(12)),
        ("DihedralGroup(4)", lambda: DihedralGroup(4)),
        ("DihedralGroup(6)", lambda: DihedralGroup(6)),
        ("SymmetricGroup(3)", lambda: SymmetricGroup(3)),
        ("SymmetricGroup(4)", lambda: SymmetricGroup(4)),
        ("AlternatingGroup(4)", lambda: AlternatingGroup(4)),
        ("AlternatingGroup(5)", lambda: AlternatingGroup(5)),
        ("QuaternionGroup()", lambda: QuaternionGroup()),
        ("KleinFourGroup()", lambda: KleinFourGroup()),
        
        # Abelian groups
        ("AbelianGroup([2,3])", lambda: AbelianGroup([2,3])),
        ("AbelianGroup([4,4])", lambda: AbelianGroup([4,4])),
        ("AbelianGroup([2,2,2])", lambda: AbelianGroup([2,2,2])),
        
        # Matrix groups
        ("GL(2,3)", lambda: GL(2,3)),
        ("GL(2,5)", lambda: GL(2,5)),
        ("SL(2,3)", lambda: SL(2,3)),
        ("SL(2,5)", lambda: SL(2,5)),
        ("SO(3,3)", lambda: SO(3,3)),
        ("Sp(4,3)", lambda: Sp(4,3)),
        ("GU(2,4)", lambda: GU(2,4)),
        ("SU(2,4)", lambda: SU(2,4)),
        ("PSL(2,7)", lambda: PSL(2,7)),
        ("PGL(2,7)", lambda: PGL(2,7)),
        
        # Permutation groups
        ("PermutationGroup([[(1,2),(3,4)], [(1,3),(2,4)]])", 
         lambda: PermutationGroup([[(1,2),(3,4)], [(1,3),(2,4)]])),
        ("PermutationGroup([[(1,2,3)], [(1,2)]])", 
         lambda: PermutationGroup([[(1,2,3)], [(1,2)]])),
        
        # Coxeter groups
        ("CoxeterGroup(['A',3])", lambda: CoxeterGroup(['A',3])),
        ("CoxeterGroup(['B',3])", lambda: CoxeterGroup(['B',3])),
        ("CoxeterGroup(['D',4])", lambda: CoxeterGroup(['D',4])),
        
        # Braid groups
        ("BraidGroup(3)", lambda: BraidGroup(3)),
        ("BraidGroup(4)", lambda: BraidGroup(4)),
        
        # Free groups
        ("FreeGroup(2)", lambda: FreeGroup(2)),
        ("FreeGroup(3)", lambda: FreeGroup(3)),
        
        # Finitely presented groups
        ("FreeGroup(2)/[FreeGroup(2)([1,2,1,-2])]", 
         lambda: FreeGroup(2)/[FreeGroup(2)([1,2,1,-2])]),
        
        # Additive groups
        ("Zmod(12)", lambda: Zmod(12)),
        ("Zmod(8)", lambda: Zmod(8)),
        
        # Graph groups
        ("graphs.CompleteGraph(4).automorphism_group()", 
         lambda: graphs.CompleteGraph(4).automorphism_group()),
        ("graphs.CycleGraph(6).automorphism_group()", 
         lambda: graphs.CycleGraph(6).automorphism_group()),
        
        # Algebraic groups over finite fields
        ("PSL(2,GF(7))", lambda: PSL(2,GF(7))),
        ("PGL(2,GF(7))", lambda: PGL(2,GF(7))),
        
        # Weyl groups
        ("WeylGroup(['A',3])", lambda: WeylGroup(['A',3])),
        ("WeylGroup(['B',3])", lambda: WeylGroup(['B',3])),
        
        # Affine groups
        ("AffineGroup(2,3)", lambda: AffineGroup(2,3)),
        
        # Crystallographic groups (if available)
        # These might not be available in all SageMath versions
    ]
    
    print("Testing automorphism group computation across SageMath group types...")
    print("=" * 80)
    
    for name, constructor in test_cases:
        try:
            # Create the group
            G = constructor()
            group_order = None
            
            # Get basic info
            try:
                group_order = G.order()
            except:
                group_order = "Unknown/Infinite"
            
            # Test automorphism group computation
            try:
                aut_group = G.automorphism_group()
                
                # Try to get automorphism group order
                try:
                    aut_order = aut_group.order()
                    status = "✓ WORKING"
                    results['working'].append((name, group_order, aut_order))
                except:
                    # Automorphism group exists but order computation fails
                    status = "⚠ PARTIAL"
                    results['partial'].append((name, group_order, "Order computation failed"))
                    
            except Exception as e:
                status = "✗ FAILING"
                results['failing'].append((name, group_order, str(e)))
                
        except Exception as e:
            status = "? UNKNOWN"
            results['unknown'].append((name, "Group creation failed", str(e)))
        
        # Print status
        print(f"{status:<12} {name:<50} Order: {str(group_order):<15}")
    
    return results

def print_detailed_report(results):
    """
    Print a detailed report of the test results.
    """
    print("\n" + "=" * 80)
    print("DETAILED REPORT")
    print("=" * 80)
    
    print(f"\n✓ WORKING ({len(results['working'])} groups):")
    print("-" * 60)
    for name, group_order, aut_order in results['working']:
        print(f"  {name:<45} |G|={group_order:<10} |Aut(G)|={aut_order}")
    
    print(f"\n⚠ PARTIAL ({len(results['partial'])} groups):")
    print("-" * 60)
    for name, group_order, issue in results['partial']:
        print(f"  {name:<45} |G|={group_order:<10} Issue: {issue}")
    
    print(f"\n✗ FAILING ({len(results['failing'])} groups):")
    print("-" * 60)
    for name, group_order, error in results['failing']:
        print(f"  {name:<45} |G|={group_order:<10}")
        print(f"    Error: {error}")
    
    print(f"\n? UNKNOWN ({len(results['unknown'])} groups):")
    print("-" * 60)
    for name, issue, error in results['unknown']:
        print(f"  {name:<45} {issue}")
        print(f"    Error: {error}")

def test_known_theorems():
    """
    Test known theoretical results about automorphism groups.
    """
    print("\n" + "=" * 80)
    print("TESTING KNOWN THEOREMS")
    print("=" * 80)
    
    theorems_passed = 0
    theorems_total = 0
    
    # Theorem: |Aut(Z/n)| = φ(n) for cyclic groups
    print("\nTheorem: |Aut(Z/n)| = φ(n) for cyclic groups")
    print("-" * 50)
    
    for n in range(2, 13):
        theorems_total += 1
        G = CyclicGroup(n)
        aut_order = G.automorphism_group().order()
        euler_phi_n = euler_phi(n)
        
        if aut_order == euler_phi_n:
            print(f"  ✓ n={n}: |Aut(Z/{n})| = {aut_order} = φ({n})")
            theorems_passed += 1
        else:
            print(f"  ✗ n={n}: |Aut(Z/{n})| = {aut_order} ≠ φ({n}) = {euler_phi_n}")
    
    # Theorem: Aut(S_n) ≅ S_n for n ≠ 6, and |Aut(S_6)| = 2|S_6|
    print(f"\nTheorem: Aut(S_n) properties")
    print("-" * 50)
    
    for n in range(3, 7):
        theorems_total += 1
        G = SymmetricGroup(n)
        aut_order = G.automorphism_group().order()
        group_order = G.order()
        
        if n == 6:
            expected_ratio = 2  # |Aut(S_6)| = 2|S_6|
        else:
            expected_ratio = 1  # |Aut(S_n)| = |S_n|
        
        actual_ratio = aut_order // group_order
        
        if actual_ratio == expected_ratio:
            print(f"  ✓ S_{n}: |Aut(S_{n})| = {actual_ratio}|S_{n}| (expected {expected_ratio})")
            theorems_passed += 1
        else:
            print(f"  ✗ S_{n}: |Aut(S_{n})| = {actual_ratio}|S_{n}| (expected {expected_ratio})")
    
    # Theorem: For abelian groups, outer automorphism groups
    print(f"\nTheorem: Abelian groups have trivial inner automorphisms")
    print("-" * 50)
    
    abelian_groups = [
        ("Z/4Z", CyclicGroup(4)),
        ("Z/6Z", CyclicGroup(6)),
        ("Z/2Z × Z/2Z", AbelianGroup([2,2])),
        ("Z/2Z × Z/4Z", AbelianGroup([2,4])),
    ]
    
    for name, G in abelian_groups:
        theorems_total += 1
        try:
            center_order = G.center().order()
            group_order = G.order()
            
            if center_order == group_order:  # Center equals the whole group
                print(f"  ✓ {name}: Center = G (all automorphisms are outer)")
                theorems_passed += 1
            else:
                print(f"  ✗ {name}: Center ≠ G (unexpected for abelian group)")
        except:
            print(f"  ? {name}: Center computation failed")
    
    print(f"\nTheorem verification: {theorems_passed}/{theorems_total} passed")
    
    return theorems_passed, theorems_total

def comprehensive_automorphism_test():
    """
    Run comprehensive tests and return a summary.
    """
    print("SageMath Automorphism Group Computation Test Suite")
    print("=" * 80)
    
    # Test all group types
    results = test_automorphism_group_computation()
    
    # Print detailed report
    print_detailed_report(results)
    
    # Test known theorems
    theorems_passed, theorems_total = test_known_theorems()
    
    # Summary
    total_working = len(results['working'])
    total_partial = len(results['partial'])
    total_failing = len(results['failing'])
    total_unknown = len(results['unknown'])
    total_tested = total_working + total_partial + total_failing + total_unknown
    
    print(f"\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Group types tested: {total_tested}")
    print(f"  ✓ Fully working: {total_working}")
    print(f"  ⚠ Partially working: {total_partial}")
    print(f"  ✗ Failing: {total_failing}")
    print(f"  ? Unknown (creation failed): {total_unknown}")
    print(f"Success rate: {(total_working)/(total_tested-total_unknown)*100:.1f}%")
    print()
    print(f"Theoretical verification: {theorems_passed}/{theorems_total} theorems passed")
    
    return results

if __name__ == "__main__":
    comprehensive_automorphism_test()