package MCP.mod_jumpblock;

import MCP.ApiController;
import MCP.BlockBase;
import net.minecraft.src.Entity;
import net.minecraft.src.Material;
import net.minecraft.src.World;

public class BlockJump extends BlockBase
{
	/**********************************************************************
	 * 
	 */
    public BlockJump(ApiController ctrl)
    {
    	// Call our inherited's class telling it
    	// we want to use the jukebox texture and
    	// have wood like properties
        super(ctrl.getBlockID(BlockJump.class), 74, Material.wood);
 
        this.setHardness(1F);
        this.setResistance(2.0F);
        this.setStepSound(soundWoodFootstep);
        this.setBlockName("jumpblock");
    }
 
	/**********************************************************************
	 * 
	 */
    public int getBlockTextureFromSide(int side)
    {
    	if(side == 1)
    	{
    		// Workshop top
    		return 43;
    	}
        return blockIndexInTexture;
    }
 
	/**********************************************************************
	 * 
	 */
    public void onEntityWalking(World world, int x, int y, int z, Entity entity)
    {
    	// Add to the entities upward velocity to send them up into the air
		entity.motionY += 2.0;
    }
}
