#!/usr/bin/env sage

def analyze_automorphism_group(G, group_name=""):
    """
    Analyze the automorphism group of G with detailed information.
    
    Parameters:
    G: A SageMath group object
    group_name: Optional name for the group
    
    Returns:
    The automorphism group, or None if computation fails
    """
    print(f"=== Automorphism Analysis: {group_name or 'Group'} ===")
    
    # Get basic group information
    try:
        group_order = G.order()
        print(f"Original group order: {group_order}")
    except:
        print("Original group order: Unknown/Infinite")
        group_order = None
    
    # Compute automorphism group with error handling
    try:
        aut_group = G.automorphism_group()
        print("✓ Automorphism group computation: SUCCESS")
    except Exception as e:
        print(f"✗ Automorphism group computation: FAILED")
        print(f"  Error: {e}")
        return None
    
    # Get automorphism group order
    try:
        aut_order = aut_group.order()
        print(f"Automorphism group order: {aut_order}")
    except:
        print("Automorphism group order: Unknown/Infinite")
        aut_order = None
    
    # Structure description
    try:
        structure = aut_group.structure_description()
        print(f"Structure: {structure}")
    except:
        print("Structure description not available")
    
    # Generators
    try:
        generators = aut_group.gens()
        print(f"Number of generators: {len(generators)}")
    except:
        print("Generator information not available")
        return aut_group
    
    # Show action on original group elements
    print("\nAutomorphism action on group elements:")
    try:
        elements = list(G)[:min(8, len(G))]  # Show first 8 elements
        
        for i, gen in enumerate(generators[:3]):  # Show first 3 generators
            print(f"  Generator {i}:")
            for elem in elements:
                try:
                    image = gen(elem)
                    if image != elem:
                        print(f"    {elem} → {image}")
                except:
                    print(f"    {elem} → (action not available)")
    except Exception as e:
        print(f"  Action display failed: {e}")
    
    return aut_group

def compare_automorphism_orders(groups_dict):
    """
    Compare automorphism group orders for multiple groups.
    
    Parameters:
    groups_dict: Dictionary {name: group} of groups to compare
    """
    print("=== Automorphism Group Order Comparison ===")
    print(f"{'Group':<20} {'Order':<8} {'Aut Order':<12} {'Ratio':<8}")
    print("-" * 50)
    
    for name, G in groups_dict.items():
        order = G.order()
        aut_order = G.automorphism_group().order()
        ratio = aut_order / order
        print(f"{name:<20} {order:<8} {aut_order:<12} {ratio:<8.2f}")

def find_inner_automorphisms(G):
    """
    Find the inner automorphism group and compare to full automorphism group.
    
    Parameters:
    G: A SageMath group object
    """
    print(f"=== Inner vs Full Automorphisms ===")
    print(f"Group order: {G.order()}")
    
    # Full automorphism group
    aut_group = G.automorphism_group()
    print(f"Full automorphism group order: {aut_group.order()}")
    
    # Inner automorphisms (conjugation by group elements)
    # Inn(G) ≅ G/Z(G) where Z(G) is the center
    try:
        center = G.center()
        center_order = center.order()
        inner_aut_order = G.order() // center_order
        
        print(f"Center order: {center_order}")
        print(f"Inner automorphism group order: {inner_aut_order}")
        print(f"Outer automorphism group order: {aut_group.order() // inner_aut_order}")
        
        # Show center elements
        print("Center elements:", list(center))
        
    except:
        print("Center computation not available for this group type")
    
    return aut_group

def automorphism_series_analysis(n_max=12):
    """
    Analyze automorphism groups for series of groups.
    
    Parameters:
    n_max: Maximum parameter for group series
    """
    print("=== Automorphism Series Analysis ===")
    
    # Cyclic groups
    print("\nCyclic groups Z/nZ:")
    print(f"{'n':<4} {'|Aut(Z/nZ)|':<12} {'φ(n)':<8}")
    print("-" * 25)
    
    for n in range(2, n_max + 1):
        G = CyclicGroup(n)
        aut_order = G.automorphism_group().order()
        euler_phi = euler_phi(n)
        print(f"{n:<4} {aut_order:<12} {euler_phi:<8}")
    
    # Dihedral groups
    print("\nDihedral groups D_n:")
    print(f"{'n':<4} {'|D_n|':<8} {'|Aut(D_n)|':<12}")
    print("-" * 25)
    
    for n in range(3, min(n_max + 1, 8)):  # Limit to avoid large computations
        G = DihedralGroup(n)
        aut_order = G.automorphism_group().order()
        print(f"{n:<4} {G.order():<8} {aut_order:<12}")

def graph_automorphism_demo():
    """
    Demonstrate automorphism computation for graphs.
    """
    print("=== Graph Automorphism Examples ===")
    
    graphs_to_test = [
        ("Complete graph K4", graphs.CompleteGraph(4)),
        ("Cycle graph C6", graphs.CycleGraph(6)),
        ("Petersen graph", graphs.PetersenGraph()),
        ("Cube graph", graphs.CubeGraph(3)),
    ]
    
    for name, graph in graphs_to_test:
        aut_group = graph.automorphism_group()
        print(f"{name}:")
        print(f"  Vertices: {graph.num_verts()}")
        print(f"  Automorphism group order: {aut_group.order()}")
        print(f"  Generators: {len(aut_group.gens())}")
        print()

# Example usage
if __name__ == "__main__":
    print("=== SageMath Automorphism Group Analysis ===\n")
    
    # Individual group analysis
    print("1. Detailed analysis of specific groups:")
    analyze_automorphism_group(CyclicGroup(8), "Z/8Z")
    print()
    
    analyze_automorphism_group(DihedralGroup(4), "D4")
    print()
    
    analyze_automorphism_group(SymmetricGroup(4), "S4")
    print()
    
    # Group comparison
    print("2. Comparison of multiple groups:")
    test_groups = {
        "Z/6Z": CyclicGroup(6),
        "Z/8Z": CyclicGroup(8),
        "D4": DihedralGroup(4),
        "S3": SymmetricGroup(3),
        "Q8": QuaternionGroup(),
    }
    compare_automorphism_orders(test_groups)
    print()
    
    # Inner automorphisms
    print("3. Inner automorphism analysis:")
    find_inner_automorphisms(DihedralGroup(4))
    print()
    
    # Series analysis
    print("4. Series analysis:")
    automorphism_series_analysis(8)
    print()
    
    # Graph automorphisms
    print("5. Graph automorphisms:")
    graph_automorphism_demo()
    
    print("\n=== Usage Notes ===")
    print("This program leverages SageMath's built-in automorphism computation")
    print("and focuses on analysis and comparison rather than reimplementation.")
    print("\nFor custom analysis:")
    print("G = YourGroup()")
    print("analyze_automorphism_group(G, 'Your Group Name')")
    print("\n=== Guarantees ===")
    print("✓ GUARANTEED: CyclicGroup, SymmetricGroup, DihedralGroup, AbelianGroup")
    print("✓ GUARANTEED: GL/SL/PSL over finite fields, QuaternionGroup, graph groups")
    print("⚠ LIKELY: PermutationGroup, CoxeterGroup, BraidGroup (finite cases)")
    print("⚡ LIMITED: FreeGroup, finitely presented groups (infinite cases)")
    print("✗ NO GUARANTEE: Custom groups, very large groups, arbitrary rings")
    print(f"\nRun full test suite: sage test_automorphism_groups.py")
    print(f"Check guarantees: sage automorphism_guarantees.py")