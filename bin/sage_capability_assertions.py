#!/usr/bin/env sage

from sage.all import *
from sage.groups.perm_gps.permgroup_named import (
    CyclicPermutationGroup,
    SymmetricGroup, 
    AlternatingGroup,
    DihedralGroup,
    QuaternionGroup,
    KleinFourGroup
)
from sage.groups.matrix_gps.all import GL, SL

def test_sage_group_capabilities():
    """
    Test what group theory capabilities are available in this SageMath installation.
    Use assertions to prove basic functionality works.
    """
    print("SageMath Group Theory Capability Tests")
    print("=" * 50)
    
    # Test 1: Basic group creation
    print("\n1. Testing basic group creation:")
    
    G = CyclicPermutationGroup(6)
    assert G.order() == 6, f"CyclicPermutationGroup(6) should have order 6, got {G.order()}"
    print(f"  ✓ CyclicPermutationGroup(6) has order {G.order()}")
    
    G = SymmetricGroup(4)
    assert G.order() == 24, f"SymmetricGroup(4) should have order 24, got {G.order()}"
    print(f"  ✓ SymmetricGroup(4) has order {G.order()}")
    
    G = DihedralGroup(4)
    assert G.order() == 8, f"DihedralGroup(4) should have order 8, got {G.order()}"
    print(f"  ✓ DihedralGroup(4) has order {G.order()}")
    
    # Test 2: Group operations
    print("\n2. Testing group operations:")
    
    G = SymmetricGroup(3)
    elements = list(G)
    assert len(elements) == 6, f"SymmetricGroup(3) should have 6 elements, got {len(elements)}"
    
    # Test identity
    identity = G.identity()
    assert identity is not None, "Group must have identity element"
    
    # Test that identity works
    gen = G.gen(0)  # First generator
    assert gen * identity == gen, "Identity must satisfy g * e = g"
    assert identity * gen == gen, "Identity must satisfy e * g = g"
    print(f"  ✓ Group operations work correctly")
    
    # Test 3: Matrix groups
    print("\n3. Testing matrix groups:")
    
    G = GL(2, 3)  # GL(2, F_3)
    order = G.order()
    expected_order = (3**2 - 1) * (3**2 - 3)  # |GL(2,q)| = (q^2-1)(q^2-q)
    assert order == expected_order, f"GL(2,3) should have order {expected_order}, got {order}"
    print(f"  ✓ GL(2,3) has correct order {order}")
    
    G = SL(2, 3)  # SL(2, F_3)  
    order = G.order()
    expected_order = 3 * (3**2 - 1)  # |SL(2,q)| = q(q^2-1)
    assert order == expected_order, f"SL(2,3) should have order {expected_order}, got {order}"
    print(f"  ✓ SL(2,3) has correct order {order}")
    
    # Test 4: Euler phi function
    print("\n4. Testing number theory functions:")
    
    assert euler_phi(6) == 2, f"φ(6) should be 2, got {euler_phi(6)}"
    assert euler_phi(12) == 4, f"φ(12) should be 4, got {euler_phi(12)}"
    assert euler_phi(7) == 6, f"φ(7) should be 6, got {euler_phi(7)}"
    print(f"  ✓ Euler phi function works correctly")
    
    # Test 5: Graph functionality
    print("\n5. Testing graph functionality:")
    
    try:
        from sage.graphs.generators.families import CompleteGraph
        from sage.graphs.generators.basic import CycleGraph
        
        # Test basic graph creation
        G = CompleteGraph(4)
        assert G.num_verts() == 4, f"Complete graph K4 should have 4 vertices, got {G.num_verts()}"
        assert G.num_edges() == 6, f"Complete graph K4 should have 6 edges, got {G.num_edges()}"
        print(f"  ✓ Graph creation works")
        
        # Test if automorphism_group exists for graphs
        if hasattr(G, 'automorphism_group'):
            aut_group = G.automorphism_group()
            aut_order = aut_group.order()
            assert aut_order == 24, f"K4 automorphism group should be S4 with order 24, got {aut_order}"
            print(f"  ✓ Graph automorphism groups work! |Aut(K4)| = {aut_order}")
            
            # Test more graphs
            cycle = CycleGraph(6)
            cycle_aut = cycle.automorphism_group()
            cycle_aut_order = cycle_aut.order()
            assert cycle_aut_order == 12, f"C6 automorphism group should be D6 with order 12, got {cycle_aut_order}"
            print(f"  ✓ Graph automorphism groups: |Aut(C6)| = {cycle_aut_order}")
            
            return True  # Automorphism groups are available for graphs
        else:
            print(f"  ⚠ Graph automorphism groups not available")
            return False
            
    except ImportError:
        print(f"  ✗ Graph functionality not available")
        return False

def test_what_automorphism_features_exist():
    """
    Test what automorphism-related features exist in this SageMath installation.
    """
    print("\n" + "=" * 50)
    print("AUTOMORPHISM FEATURE DETECTION")
    print("=" * 50)
    
    # Test groups for automorphism_group method
    test_groups = [
        ("SymmetricGroup(4)", SymmetricGroup(4)),
        ("CyclicPermutationGroup(6)", CyclicPermutationGroup(6)),
        ("DihedralGroup(4)", DihedralGroup(4)),
        ("GL(2,3)", GL(2,3)),
    ]
    
    has_automorphisms = False
    
    for name, G in test_groups:
        if hasattr(G, 'automorphism_group'):
            print(f"  ✓ {name} has automorphism_group() method")
            try:
                aut_group = G.automorphism_group()
                print(f"    |Aut({name})| = {aut_group.order()}")
                has_automorphisms = True
            except Exception as e:
                print(f"    ⚠ Method exists but failed: {e}")
        else:
            print(f"  ✗ {name} has no automorphism_group() method")
    
    # Check if GAP is available and has automorphism functionality
    print(f"\nChecking GAP integration:")
    try:
        import sage.libs.gap.libgap as libgap
        gap = libgap.gap
        
        # Test if we can access GAP's automorphism functions
        G = SymmetricGroup(4)
        gap_group = G._gap_()
        
        if hasattr(gap_group, 'AutomorphismGroup'):
            print(f"  ✓ GAP automorphism functions accessible")
            aut_gap = gap_group.AutomorphismGroup()
            print(f"    GAP: |Aut(S4)| = {aut_gap.Size()}")
            has_automorphisms = True
        else:
            print(f"  ✗ GAP automorphism functions not accessible")
            
    except Exception as e:
        print(f"  ✗ GAP integration issue: {e}")
    
    return has_automorphisms

def main():
    """
    Main function that tests SageMath capabilities with assertions.
    """
    print("Testing SageMath Installation Capabilities")
    print("This will crash if basic functionality doesn't work!")
    print()
    
    # Test basic functionality
    test_sage_group_capabilities()
    
    # Test automorphism features
    has_auto = test_what_automorphism_features_exist()
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    if has_auto:
        print("✅ SUCCESS: This SageMath installation has automorphism group functionality!")
        print("You can proceed with automorphism group computations.")
    else:
        print("⚠️  LIMITED: This SageMath installation has basic group theory but")
        print("   no automorphism group computation capabilities.")
        print("   You may need a different SageMath build or additional packages.")
    
    print("\n✅ All basic assertions passed - SageMath core functionality works!")

if __name__ == "__main__":
    main()